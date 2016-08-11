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

    def __str__(self):
        text = '\nGitHub ID: {}\n'.format(self.rgo.admin.ghid)
        text += 'GitHub token file: {}\n'.format(self.rgo.admin.token_file)
        text += 'Organization name: {}\n'.format(self.rgo.org.name)
        text += 'Roster file: {}\n'.format(self.rgo.roster.path)
        text += 'Local master repo.: {}\n'.format(self.lgo.master_repo)
        text += 'Local student repo. directory: {}\n'.format(self.lgo.student_repo_dir)
        return text
    
    def _storeGitRoomInfo(self):
        
        while True:
            odir = input('Please give directory for saving: ').strip()
            
            try:
                odir = os.path.expanduser(odir)
                
            except AttributeError:
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

                self.rgo.getMembers()
                self.rgo.getTeams()
                self.rgo.getRepos()

            else:
                prompt = 'Would you like to try again?'
                choice = pickOpt(prompt, ['Yes','No'])
                if choice == 0:
                    self._initGitRoom(github_login = None, token_file = None,
                                      orgname = None, roster_file = None,
                                      master_repo = None, student_repo_dir = None)
                else:
                    progExit()
                    
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

            self._initGitRoom(github_login = info['github_login'],
                              token_file = info['github_token_file'],
                              orgname = info['organization_name'],
                              roster_file = info['roster_file'],
                              master_repo = info['master_repo'],
                              student_repo_dir = info['student_repo_dir'])

    def getGitRoomObjs(self):
        if self.rgo and self.lgo:
            return
        else:
            while True:
                prompt = 'How would you like to enter GitRoom information?'
                opts = ['Manually', 'From JSON file']
                choice = pickOpt(prompt, opts)
                if choice == 0:
                    self._initGitRoom()
                else:
                    prompt = 'Please give path to GitRoom JSON file: '
                    grjson = os.path.expanduser(input(prompt).strip())
                    if os.path.isfile(grjson):
                        self._readGitRoomInfo(grjson)
                        break
                    else:
                        errorMessage('Not a file!')
                        continue

    # ----------------------------------
    # GitRoom main menu choices
    # ----------------------------------

    def buildGR(self, from_scratch = False):

        __rb = 'https://github.com/'

        to_add = []

        if from_scratch:
            for k,v in self.rgo.roster.students.items():
                to_add.append(k)
        else:
            # compare roster to remote
            current = []
            for k,v in self.rgo.org.members.items():
                current.append(v.ghid)
                
            for k,v in self.rgo.roster.students.items():
                if v.ghid not in current:
                    to_add.append(k)
 
        m = 'Students to be added to {}'.format(self.rgo.org.name)
        promptMessage(m, char = '')
        for name in to_add:
            fn = self.rgo.roster.students[name].first_name
            ln = self.rgo.roster.students[name].last_name
            print('{} {}'.format(fn, ln))

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
            self.rgo.addMember(member = name)
            # 2
            self.rgo.createRemoteRepo(repo_name = rn)
            # 3
            resp = self.rgo.createTeam(team_name = rn)
            team = Team(team_id = resp['id'], name = resp['name'])
            if team.name:
                self.rgo.org.teams[team.name] = team
            # 4
            self.rgo.addMemberToTeam(team_name = rn, member = name)
            mem = Member(ghid = gh)
            members = {}
            members[gh] = mem
            if team.name:
                self.rgo.org.teams[team.name].members = members
            # 5
            resp = self.rgo.addRepoToTeam(team_name = rn, repo_name = rn)
            # 6
            self.lgo.createLocalRepo(student_repo = rn)
            # 7
            self.lgo.masterToStudent(student_repo = rn)
            # 8
            remote = '{}{}/{}.git'.format(__rb, self.rgo.org.name, rn)
            self.lgo.gitInit(repo = rp)
            self.lgo.gitRemoteAdd(repo = rp, remote = remote)
            self.lgo.gitAdd(repo = rp)
            self.lgo.gitCommit(repo = rp, message = 'Init course repo')
            self.lgo.gitPush(repo = rp)

    def addGRAdmin(self):

        prompt = 'Please give new administrator\'s GitHub id: '
        ghid = input(prompt).strip()
        self.rgo.addAdmin(github_id = ghid)

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
            remote = '{}{}/{}.git'.format(__rb, self.rgo.org.name, k)
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
