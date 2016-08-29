# gr.py
# -*- coding: utf-8 -*-

from .utils import *
from .api import *
from .loc import *

import json
import os

class GR:

    '''
    Class for GitRoom initialization/reading functions
    '''

    def __init__(self, rgo = None, lgo = None):
        self.rgo = rgo
        self.lgo = lgo
        self.__rb = 'https://github.com/'

    def __str__(self):
        text = '\nGitHub ID: {}\n'.format(self.rgo.admin.ghid)
        text += 'GitHub token file: {}\n'.format(self.rgo.admin.token_file)
        text += 'Organization name: {}\n'.format(self.rgo.org.name)
        text += 'Roster file: {}\n'.format(self.rgo.roster.path)
        text += 'Local master repo.: {}\n'.format(self.lgo.master_repo)
        text += 'Local student repo. directory: {}\n'.format(self.lgo.student_repo_dir)
        return text

    def _updateGitRoom(self):
        print('\nGetting information from organization remote...')
        self.rgo.getMembers()
        self.rgo.getTeams()
        self.rgo.getRepos()
        return 0
    
    def _storeGitRoomInfo(self):
        
        while True:
            prompt = 'Please give directory for saving: '
            odir = os.path.expanduser(input(prompt).strip())
            if not os.path.isdir(odir):
                errorMessage('Please input a directory path.')
                continue
            
            info = {'github_login': self.rgo.admin.ghid,
                    'github_token_file': self.rgo.admin.token_file,
                    'organization_name': self.rgo.org.name,
                    'roster_file': self.rgo.roster.path,
                    'master_repo': self.lgo.master_repo,
                    'student_repo_dir': self.lgo.student_repo_dir}
            
            with open(odir + '/' + self.rgo.org.name + '_grm.json', 'w') as f:
                json.dump(info, f, indent = 4)
                
            break

    def _initGitRoom(self, github_login = None, token_file = None,
                     orgname = None, roster_file = None, master_repo = None,
                     student_repo_dir = None):

        # remote git inits
        self.rgo = RemoteGit()
        self.rgo.setAPICreds(ghid = github_login, tokenfile = token_file)
        self.rgo.setOrg(name = orgname)
        self.rgo.buildRoster(rosterfile = roster_file)
        
        # local git inits
        self.lgo = LocalGit()
        self.lgo.set_master_repo(master_repo = master_repo)
        self.lgo.set_student_repo_dir(student_repo_dir = student_repo_dir)

        # option to store inits if any were missing
        if (not github_login or not token_file or not orgname
            or not roster_file or not master_repo or not student_repo_dir):
            print('*' * 50)
            print('\nThis is what you have entered:\n')
            print(self)
            print('*' * 50)
            prompt = 'Is this correct?'
            choice = pickOpt(prompt, ['Yes','No'])
            if choice == 0:
                prompt = 'Do you want to store GitRoom information in JSON file?'
                choice = pickOpt(prompt, ['Yes','No'])
                if choice == 0:
                    self._storeGitRoomInfo()

            else:
                prompt = 'Would you like to try again?'
                choice = pickOpt(prompt, ['Yes','No'])
                if choice == 0:
                    self._initGitRoom(github_login = None, token_file = None,
                                      orgname = None, roster_file = None,
                                      master_repo = None, student_repo_dir = None)
                else:
                    progExit()

        try:
            self.rgo.getMembers()

        except requests.exceptions.ConnectionError:
            errorMessage('Not able to connect to remote.')
            return 1

        return self._updateGitRoom()
                    
    def _readGitRoomInfo(self, init_file_path):
        
        with open(init_file_path, 'r') as f:
            info = json.load(f)
            
            req_keys = ['github_login', 'github_token_file',
                        'organization_name', 'roster_file',
                        'master_repo', 'student_repo_dir']

            for k in req_keys:
                try:
                    info[k]
                except KeyError:
                    info[k] = None               

            connect_code = self._initGitRoom(github_login = info['github_login'],
                                             token_file = info['github_token_file'],
                                             orgname = info['organization_name'],
                                             roster_file = info['roster_file'],
                                             master_repo = info['master_repo'],
                                             student_repo_dir = info['student_repo_dir'])
            return connect_code

    def getGitRoomObjs(self, connect_code):
        if self.rgo and self.lgo:
            if connect_code != 0:
                try:
                    self.rgo.getMembers()
                except requests.exceptions.ConnectionError:
                    return 1
                return self._updateGitRoom()
            else:
                return 0    
        else:
            while True:
                prompt = 'How would you like to enter GitRoom information?'
                opts = ['Manually', 'From JSON file', '<< Exit Program >>']
                choice = pickOpt(prompt, opts)
                if choice == len(opts) - 1:
                    progExit()
                elif choice == 0:
                    self._initGitRoom()
                else:
                    prompt = 'Please give path to GitRoom JSON file: '
                    grjson = os.path.expanduser(input(prompt).strip())
                    if os.path.isfile(grjson):
                        connect_code = self._readGitRoomInfo(grjson)
                        return connect_code
                    else:
                        errorMessage('Not a file!')
                        continue

    # ----------------------------------
    # GitRoom main menu choices
    # ----------------------------------

    def buildGR(self, from_scratch = False):

        to_add = []

        if not from_scratch:
            # compare roster to remote
            current = []
            for k,v in self.rgo.org.members.items():
                current.append(v.ghid)
                
            for k,v in self.rgo.roster.students.items():
                if v.ghid not in current:
                    to_add.append(k)
        else:
            for k,v in self.rgo.roster.students.items():
                to_add.append(k)

        if len(to_add) == 0:
            print('All local students on remote')
            return
 
        m = 'Students to be added to {}'.format(self.rgo.org.name)
        promptMessage(m, char = '')
        for name in to_add:
            fn = self.rgo.roster.students[name].first_name
            ln = self.rgo.roster.students[name].last_name
            print('{} {}'.format(fn, ln))

        prompt = 'Should repos be private?'
        choice = pickOpt(prompt, ['Yes','No'])
        if choice == 0:
            priv_bool = True
        else:
            priv_bool = False

        # STEPS
        # 1. [Remote] Add student as GitRoom member
        # 2. [Remote] Init remote repo
        # 3. [Remote] Add team for student's repo       
        # 4. [Remote] Add student to team
        # 5. [Remote] Add repo to team
        # 6. [Local] Create student's local repo
        # 7. [Local] Copy files from master to student's repo
        # 8. [Local] Add, commit, push local student repo to remote
        
        for name in to_add:
            ln = self.rgo.roster.students[name].last_name
            gh = self.rgo.roster.students[name].ghid
            rn = 'student_{}'.format(ln.lower())
            rp = os.path.join(self.lgo.student_repo_dir, rn)

            # 1
            resp = self.rgo.addMember(member = name)

            if round(resp.status_code, -2) == 400:
                print(resp.json()['message'])
            elif resp.json()['state'] == 'active':
                print('{} is already an active member.'.format(name))
            elif resp.json()['state'] == 'pending':
                print('{} has a pending membership.'.format(name))

            # 2
            resp = self.rgo.createRemoteRepo(repo_name = rn, private = priv_bool)

            if resp.status_code == 422:
                text = '\nEither:\n\n'
                text += '(1) Remote already exists\n'
                text += '(2) Your organization plan doesn\'t allow for private repos \n'
                text += '    and you must change the setting to public \n'
                text += '    or upgrade your plan through GitHub.'
                errorMessage(text)        
            elif round(resp.status_code, -2) == 200:
                print('Successfully created remote {}'.format(rn))

            # 3
            resp = self.rgo.createTeam(team_name = rn)

            if resp.status_code == 422:
                print('Team {} already exists!\n'.format(rn))                      
            elif round(resp.status_code, -2) == 200:
                print('Successfully created team: {}'.format(rn))
                resp = resp.json()            
                team = Team(team_id = resp['id'], name = resp['name'])
                self.rgo.org.teams[team.name] = team

            # 4
            resp = self.rgo.addMemberToTeam(team_name = rn, member = name)

            if round(resp.status_code, -2) == 200:
                state = resp.json()['state']
                print('{}\'s membership on team {} is now {}.'.format(name,
                                                                      rn,
                                                                      state))
                mem = Member(ghid = gh)
                members = {}
                members[gh] = mem

            # 5
            resp = self.rgo.addRepoToTeam(team_name = rn, repo_name = rn)

            if round(resp.status_code, -2) == 200:
                print('{} now has access to repo {}'.format(rn, rn))

            # 6
            self.lgo.createLocalRepo(student_repo = rn)

            # 7
            self.lgo.masterToStudent(student_repo = rn)

            # 8
            remote = '{}{}/{}.git'.format(self.__rb, self.rgo.org.name, rn)
            self.lgo.gitInit(repo = rp)
            self.lgo.gitRemoteAdd(repo = rp, remote = remote)
            self.lgo.gitAdd(repo = rp)
            self.lgo.gitCommit(repo = rp, message = 'Init course repo')
            self.lgo.gitPush(repo = rp)

    def addGRAdmin(self):

        prompt = 'Please give new administrator\'s GitHub id: '
        ghid = input(prompt).strip()
        resp = self.rgo.addAdmin(github_id = ghid)

        if round(resp.status_code, -2) == 400:
            errorMessage(resp.json()['message'])
        elif round(resp.status_code, -2) == 200:
            print('Successfully added {} to {} as admin.'.format(ghid,
                                                                 self.org.name))

    def cloneGR(self):
        self.rgo.getRepos()
        while True:
            prompt = 'Please give path to local clone directory: '
            cdir = input(prompt).strip()
            try:
                cdir = os.path.expanduser(cdir)
                
            except AttributeError:
                errorMessage('Please give a proper path.')
                continue
            
            cdir = cdir.rstrip('/')
            break
        
        for k,v in self.rgo.org.repos.items():
            repo = os.path.join(cdir, k)
            remote = '{}{}/{}.git'.format(self.__rb, self.rgo.org.name, k)
            self.lgo.gitClone(repo = repo, remote = remote)

    def updateGR(self):
        self.rgo.getRepos()
        while True:
            prompt = 'Please enter commit message: '
            comment = input(prompt).strip()
            prompt = 'Is this okay or do you want to try again?\n\n'
            prompt += 'COMMENT: {}'.format(comment)
            choice = pickOpt(prompt, ['Good', 'Try again'])
            if choice == 0:
                break

        for k,v in self.rgo.org.repos.items():
            repo = k
            repo_path = os.path.join(self.lgo.student_repo_dir, repo)
            if not os.path.isdir(repo_path):
                continue
            self.lgo.gitPull(repo = repo_path)
            self.lgo.masterToStudent(student_repo = repo)
            self.lgo.gitAdd(repo = repo_path)
            self.lgo.gitCommit(repo = repo_path, message = comment)
            self.lgo.gitPush(repo = repo_path)  

    def pullGR(self):
        self.rgo.getRepos()

        prompt = 'Please select the student repository you wish to pull'
        opts = ['-- All student repositories --']
        for k,v in self.rgo.org.repos.items():
            repo = os.path.join(self.lgo.student_repo_dir, k)
            if not os.path.isdir(repo):
                continue
            opts.append(k)

        choice = pickOpt(prompt, opts)
        if choice == 0:
            for k,v in self.rgo.org.repos.items():
                repo_path = os.path.join(self.lgo.student_repo_dir, k)
                if not os.path.isdir(repo_path):
                    continue
                self.lgo.gitPull(repo = repo_path)
        else:
            repo_path = os.path.join(self.lgo.student_repo_dir, opts[choice])
            self.lgo.gitPull(repo = repo_path)

    def pushGR(self):
        self.rgo.getRepos()

        prompt = 'Please select the student repository you wish to push'
        opts = ['-- All student repositories --']
        for k,v in self.rgo.org.repos.items():
            repo_path = os.path.join(self.lgo.student_repo_dir, k)
            if not os.path.isdir(repo_path):
                continue
            opts.append(k)

        choice = pickOpt(prompt, opts)
            
        while True:
            comment = input('Please enter commit message: ').strip()
            prompt = 'Is this okay or do you want to try again?\n\n'
            prompt += 'COMMENT: {}'.format(comment)
            select = pickOpt(prompt, ['Good', 'Try again'])
            if select == 0:
                break
            
        if choice == 0:
            for k,v in self.rgo.org.repos.items():
                repo_path = os.path.join(self.lgo.student_repo_dir, k)
                if not os.path.isdir(repo_path):
                    continue
                self.lgo.gitPull(repo = repo_path)
                self.lgo.gitAdd(repo = repo_path)
                self.lgo.gitCommit(repo = repo_path, message = comment)
                self.lgo.gitPush(repo = repo_path)
        else:
            repo_path = os.path.join(self.lgo.student_repo_dir, opts[choice])
            self.lgo.gitPull(repo = repo)
            self.lgo.gitPull(repo = repo_path)
            self.lgo.gitAdd(repo = repo_path)
            self.lgo.gitCommit(repo = repo_path, message = comment)
            self.lgo.gitPush(repo = repo_path)
