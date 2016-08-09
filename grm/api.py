# api.py
# -*- coding: utf-8 -*-

import getpass
import os
import pandas as pd
import requests

from .utils import *

gh_api = 'https://api.github.com/'

class Admin:

    '''
    Class for primary GitHub Classrom management functions
    '''
    
    def __init__(self, ghid = None, token_file = None, token = None):
        self.ghid = ghid
        self.token_file = token_file
        self.__token = token

    def __str__(self):
        t = None if self.__token is None else '[ Hidden ]'
        text = '\nGitHub ID:  {}\n'.format(self.ghid)
        text +=  'Token path: {}\n'.format(self.token_file)
        text +=  'Token:      {}\n'.format(t)
        return text
      

class Org:

    '''
    Class for GitHub organization
    '''

    def __init__(self, name = None, repos = None, members = None, teams = None):
        self.name = name
        self.repos = repos if isinstance(repos, dict) else {}
        self.members = members if isinstance(members, dict) else {}
        self.teams = teams if isinstance(teams, dict) else {}

    def __str__(self):
        text = '\nOrg Name: {0}\n'.format(self.name)
        if self.repos:
            text +=  '\nRepos:\n'
            for k,v in sorted(self.repos.items()):
                text += str(Repository(name = v.name, repo_id = v.repo_id))
        if self.members:
            text +=  '\nMembers:\n'
            for k,v in sorted(self.members.items()):
                text += str(Member(ghid = v.ghid, role = v.role))
        if self.teams:
            text +=  '\nTeams:\n'
            for k,v in sorted(self.teams.items()):
                text += str(Team(name = v.name, team_id = v.team_id,
                                 repos = v.repos, members = v.members))
        return text


class Repository:

    '''
    Class for repository information
    '''

    def __init__(self, name = None, repo_id = None):
        self.name = name
        self.repo_id = repo_id

    def __str__(self):
        return '\nRepo Name: {}; Repo ID: {}\n'.format(self.name, self.repo_id)


class Member:

    '''
    Class for GitHub organization member
    '''

    def __init__(self, ghid = None, role = None):
        self.ghid = ghid
        self.role = role

    def __str__(self):
        if self.role:
            return '{} [{}]\n'.format(self.ghid, self.role)
        else:
            return '{}\n'.format(self.ghid)


class Team:

    '''
    Class for GitHub organization team
    '''

    def __init__(self, team_id = None, name = None, repos = None, members = None):
        self.team_id = team_id
        self.name = name
        self.repos = repos if isinstance(repos, dict) else {}
        self.members = members if isinstance(members, dict) else {}

    def __str__(self):
        text = '\nTeam Name: {}; Team ID: {}\n'.format(self.name, self.team_id)
        for k,v in sorted(self.repos.items()):
            text += str(Repository(name = v.name, repo_id = v.repo_id))
        for k,v in sorted(self.members.items()):
            text += str(Member(ghid = v.ghid, role = v.role))
        return text


class Roster:
            
    '''
    Class for course roster information
    '''

    def __init__(self, path = None):
        self.path = path
        self.students = {}

    def __str__(self):
        text =  '\nPath:   {0}\n'.format(self.path)
        text +=   'Students: '
        for k,v in sorted(self.students.items()):
            text += str(Student(first_name = v.first_name,
                                last_name = v.last_name,
                                ghid = v.ghid))
        return text


class Student:

    '''
    Class for single student information
    '''

    def __init__(self, first_name = None, last_name = None, ghid = None):
        self.first_name = first_name
        self.last_name = last_name
        self.ghid = ghid

    def __str__(self):
        return '{} {} [{}]; '.format(self.first_name, self.last_name, self.ghid)


class RemoteGit:

    '''
    Remote git management operations
    '''
    
    def __init__(self):
        self.admin = None
        self.org = None
        self.roster = None

    def __str__(self):
        text = '\nAdmin:\n {}\n'.format(self.admin)
        text += '\nOrganization:\n {}\n'.format(self.org)
        text += '\nRoster:\n {}\n'.format(self.roster)
        return text

    # ------------------------
    # Admin functions
    # ------------------------

    def setLogin(self, ghid = None, **kwargs):
        if not ghid:
            return input('Please enter your GitHub id: ').strip()
        else:
            return ghid
                          
    def setToken(self, tokenfile = None, **kwargs):
        if tokenfile is not None:
            tfp = os.path.expanduser(tokenfile) 
            with open(tfp) as f:
                return tfp, f.read().strip()
        while True:
            tfp = input('Please enter path to token file: ').strip()
            tfp = os.path.expanduser(tfp)
            if os.path.isfile(tfp):
                with open(tfp) as f:
                    return tfp, f.read().strip()
            else:
                errorMessage('Not a proper file!')
                continue

    def setAPICreds(self, **kwargs):
        admin = Admin()
        admin.ghid = self.setLogin(**kwargs)
        admin.token_file, admin._Admin__token = self.setToken(**kwargs)
        self.admin = admin

    def setOrg(self, **kwargs):
        org = Org(**kwargs)
        if not org.name:
            mess = 'Please enter your organization name: '
            org.name = input(mess)
        self.org = org

    # ------------------------
    # Roster functions
    # ------------------------

    def readRosterCSV(self, rosterpath):
        rpath = os.path.expanduser(rosterpath)
        df = pd.read_csv(rpath)
        return df, rpath

    def buildRoster(self, rosterfile = None, **kwargs):

        rost = Roster(**kwargs)
        if rosterfile:
            roster, rpath = self.readRosterCSV(rosterfile)
        else:
            while True:
                mess = 'Please enter path to roster CSV file: '
                rosterfile = os.path.expanduser(input(mess).strip())
                if os.path.isfile(rosterfile):
                    roster, rpath = self.readRosterCSV(rosterfile)
                    break
                else:
                    errorMessage('Not a proper file!')
                    continue         

        rost.path = rpath

        # allow for different column names in roster file
        icols = list(roster.columns.values)
        ocols = {'first_name': 'first name',
                 'last_name': 'last name',
                 'ghid': 'GitHub ID'}
        miss = list(set(['first_name','last_name','ghid']) - set(icols))
        corr = {}
        for k,v in ocols.items():
            if k in miss:
                mess = 'Which roster column is the student\'s ' + v + '?'
                choice = pickOpt(mess, icols)
                corr[k] = choice
            else:
                corr[k] = roster.columns.get_loc(k)
                      
        for index, row in roster.iterrows():
            student = Student(first_name = row[corr['first_name']],
                              last_name = row[corr['last_name']],
                              ghid = row[corr['ghid']])
            key = student.last_name + '_' + student.first_name
            rost.students[key] = student
        self.roster = rost

        # option to rename roster names to match GitRoom requirements
        if len(miss) > 0:
            p = 'Do you want rename you roster file columns with GitRoom names?'
            choice = pickOpt(p, ['Yes', 'No'])
            if choice == 0:
                old = [icols[corr['last_name']],
                       icols[corr['first_name']],
                       icols[corr['ghid']]]
                roster.rename(columns = {old[0]:'last_name',
                                         old[1]:'first_name',
                                         old[2]:'ghid'},
                              inplace = True)
                roster.to_csv(rpath, index = False)

    # ------------------------
    # Requests API
    # ------------------------

    def getGR(self, url, **kwargs):
        auth = (self.admin.ghid, self.admin._Admin__token)
        resp = requests.get(url, auth = auth, **kwargs)
        return resp.json()

    def postGR(self, url, **kwargs):
        auth = (self.admin.ghid, self.admin._Admin__token)
        resp = requests.post(url, auth = auth, **kwargs)
        return resp

    def putGR(self, url, **kwargs):
        auth = (self.admin.ghid, self.admin._Admin__token)
        resp = requests.put(url, auth = auth, **kwargs)
        return resp 
        
    # ------------------------
    # Org functions: get
    # ------------------------

    def getMembers(self):
        url = gh_api + 'orgs/' + self.org.name + '/members'
        resp = self.getGR(url, params = {'role':'admin'})
        ad_members = {}
        for r in resp:
            ghid = r['login']
            member = Member(ghid = ghid, role = 'admin')
            ad_members[ghid] = member
        resp = self.getGR(url, params = {'role':'member'})
        members = {}
        for r in resp:
            ghid = r['login']
            member = Member(ghid = ghid, role = 'member')
            members[ghid] = member
        members.update(ad_members)
        self.org.members = members

    def getTeams(self):
        url = gh_api + 'orgs/' + self.org.name + '/teams'
        resp = self.getGR(url)
        teams = {}
        for r in resp:
            team = Team(team_id = r['id'], name = r['name'])
            url = gh_api + 'teams/' + str(team.team_id) + '/members'
            resp = self.getGR(url)
            members = {}
            for r in resp:
                ghid = r['login']
                member = Member(ghid = ghid)
                members[ghid] = member
            team.members = members
            url = gh_api + 'teams/' + str(team.team_id) + '/repos'
            resp = self.getGR(url)
            repos = {}
            for r in resp:
                repo = Repository(name = r['name'], repo_id = r['id'])
                repos[r['name']] = repo
            team.repos = repos
            teams[team.name] = team
        self.org.teams = teams
            
    def getRepos(self):
        url = gh_api + 'orgs/' + self.org.name + '/repos'
        resp = self.getGR(url)
        repos = {}
        for r in resp:
            repo = Repository(name = r['name'], repo_id = r['id'])
            repos[r['name']] = repo
        self.org.repos = repos

    # ------------------------
    # Org functions: post/put
    # ------------------------

    def createRemoteRepo(self, repo_name):
        url = gh_api + 'orgs/' + self.org.name + '/repos'
        json = {'name': repo_name, 'private':'true'}
        resp = self.postGR(url, json = json)
        if round(resp.status_code, -2) == 200:
            print('Successfully created remote {}'.format(repo_name))

    def addMember(self, member, role = 'member'):
        mid = str(self.roster.students[member].ghid)
        url = gh_api + 'orgs/' + self.org.name + '/memberships/' + mid
        params = {'role': role}
        resp = self.putGR(url, params = params)
        if round(resp.status_code, -2) == 200:
            print('Successfully added {} to {}.'.format(member,self.org.name))

    def addAdmin(self, github_id):
        url = gh_api + 'orgs/' + self.org.name + '/memberships/' + github_id
        params = {'role': 'admin'}
        resp = self.putGR(url, params = params)
        if round(resp.status_code, -2) == 200:
            print('Successfully added {} to {} as admin.'.format(github_id,
                                                                 self.org.name))
                                
    def createTeam(self, team_name, permission = 'push'):
        url = gh_api + 'orgs/' + self.org.name + '/teams'
        json = {'name': team_name, 'permission': permission}
        resp = self.postGR(url, json = json)
        if round(resp.status_code, -2) == 200:
            print('Successfully created team: {}'.format(team_name))
            return resp.json()

    def addMemberToTeam(self, team_name, member, role = 'member'):
        mid = str(self.roster.students[member].ghid)
        tid = str(self.org.teams[team_name].team_id)
        url = gh_api + 'teams/' + tid + '/memberships/' + mid
        params = {'role': role}
        resp = self.putGR(url, params = params)
        if round(resp.status_code, -2) == 200:
            state = resp.json()['state']
            print('{}\'s membership on team {} is now {}.'.format(member,
                                                                  team_name,
                                                                  state))
     
    def addRepoToTeam(self, team_name, repo_name):
        tid = str(self.org.teams[team_name].team_id)
        url = gh_api + 'teams/' + tid + '/repos/' + self.org.name
        url += '/' + repo_name
        params = {'permission': 'push'}
        resp = self.putGR(url, params = params)
        if round(resp.status_code, -2) == 200:
            print('{} now has access to repo {}'.format(team_name, repo_name))
        
        
