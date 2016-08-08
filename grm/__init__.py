# __init__.py
# -*- coding: utf-8 -*-

version = '0.1.0'

from .api import Admin, Org, Student, Member, Repository, Roster, Team, RemoteGit
from .sys import LocalGit
from .utils import *
from .img import *

import json
import os
import subprocess as sp

def storeGitRoomInfo(gro, lmo):
    '''
    gro := GitRoom object
    lmo := local machine object
    '''
    
    while True:
        prompt = 'Please give directory for saving: '
        odir = input(str(prompt)).strip()
        
        try:
            odir = os.path.expanduser(odir)
            
        except AttributeError:
            errorMessage('Please input a directory path.')
            continue
        
        info = {'github_login': gro.admin.ghid,
                'github_token_file': gro.admin.token_file,
                'organization_name': gro.org.name,
                'roster_file': gro.roster.path,
                'master_repo': lmo.master_repo,
                'student_repo_dir': lmo.student_repo_dir}
        
        with open(odir + '/' + gro.org.name + '_gitroom_info.json', 'w') as f:
            json.dump(info, f, indent = 4)
            
        break

def initGitRoom(github_login = None, token_file = None, orgname = None,
                roster_file = None, master_repo = None,
                student_repo_dir = None):

    # GitRoom object
    gro = RemoteGit()
    gro.setAPICreds(ghid = github_login, tokenfile = token_file)
    gro.setOrg(name = orgname)
    gro.buildRoster(roster = roster_file)
    gro.getMembers()
    gro.getTeams()
    gro.getRepos()

    # local machine object
    lmo = LocalGit()
    lmo.set_master_repo(master_repo = master_repo)
    lmo.set_student_repo_dir(student_repo_dir = student_repo_dir)

    if (not github_login or not token_file or not orgname
        or not roster_file or not master_repo or not student_repo_dir):
        prompt = 'Do you want to store GitRoom information in JSON file?'
        choice = pickOpt(prompt, ['Yes','No'])
        if choice == 0:
            storeGitRoomInfo(gro, lmo)
    
    return gro, lmo
        
def readGitRoomInfo():

    while True:
        prompt = 'Please give path to GitRoom information file: '
        idir = input(str(prompt)).strip()
        
        try:
            idir = os.path.expanduser(idir)
            
        except AttributeError:
            errorMessage('Please input a proper path.')
            continue
            
        with open(idir, 'r') as f:
            info = json.load(f)

            req_keys = ['github_login', 'github_token_file',
                        'organization_name', 'roster_file',
                        'master_repo', 'student_repo_dir']

            for k in req_keys:
                try:
                    info[k]
                except KeyError:
                    info[k] = None               

            gro, lmo = initGitRoom(github_login = info['github_login'],
                                   token_file = info['github_token_file'],
                                   orgname = info['organization_name'],
                                   roster_file = info['roster_file'],
                                   master_repo = info['master_repo'],
                                   student_repo_dir = info['student_repo_dir'])
            
            return gro, lmo

def getGitRoomObjs(gro = None, lmo = None):
    if gro and lmo:
        return gro, lmo
    else:
        prompt = 'How would you like to enter GitRoom information?'
        opts = ['Manually', 'From JSON file']
        choice = pickOpt(prompt, opts)
        if choice == 0:
            gro, lmo = initGitRoom()
        else:
            gro, lmo = readGitRoomInfo()
        return gro, lmo
    

def main():

    print(startup.format(version))
    
    # init empty GitRoom objects
    gro, lmo = None, None

    __rb = 'https://github.com/'
            
    while True:
        # starting menu
        prompt = 'What would you like to do?'
        opts = ['Initialize class',
                'Add students to class',
                'Add new administrator',
                'Clone repositories',
                'Update student remote repositories with local master',
                'Pull down from remote student repositories',
                'Push from local student repositories to remotes',
                'Grade student assignments']
        choice = pickOpt(prompt, opts)

        if choice == 7:
            prompt = 'Do you need to pull from student repos?'
            select = pickOpt(prompt, ['Yes', 'No'])
            if select == 0:
                gro, lmo = getGitRoomObjs(gro, lmo)
        else:
            gro, lmo = getGitRoomObjs(gro, lmo)
                             
        # (0) Initialize class; (1) Add students to class
        if choice <= 1:

            to_add = []

            if choice == 1:
                # compare roster to remote
                current = []
                for k,v in gro.org.members.items():
                    current.append(v.ghid)
                
                for k,v in gro.roster.students.items():
                    if v.ghid not in current:
                        to_add.append(k)
            else:
                for k,v in gro.roster.students.items():
                    to_add.append(k)

            m = 'Students to be added to {}'.format(gro.org.name)
            promptMessage(m, char = '.')
            for name in to_add:
                fn = gro.roster.students[name].first_name
                ln = gro.roster.students[name].last_name
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
                ln = gro.roster.students[name].last_name
                gh = gro.roster.students[name].ghid
                rn = 'student_{}'.format(ln.lower())
                rp = os.path.join(lmo.student_repo_dir, rn)
                # 1
                gro.addMember(member = name)
                # 2
                gro.createRemoteRepo(repo_name = rn)
                # 3
                resp = gro.createTeam(team_name = rn)
                team = Team(team_id = resp['id'], name = resp['name'])
                gro.org.teams[team.name] = team
                # 4
                gro.addMemberToTeam(team_name = rn, member = name)
                mem = Member(ghid = gh)
                members = {}
                members[gh] = mem
                gro.org.teams[team.name].members = members
                # 5
                resp = gro.addRepoToTeam(team_name = rn, repo_name = rn)
                # 6
                lmo.createLocalRepo(student_repo = rn)
                # 7
                lmo.masterToStudent(student_repo = rn)
                # 8
                remote = '{}{}/{}.git'.format(__rb, gro.org.name, rn)
                lmo.gitInit(repo = rp)
                lmo.gitRemoteAdd(repo = rp, remote = remote)
                lmo.gitAdd(repo = rp)
                lmo.gitCommit(repo = rp, message = 'Init course repo')
                lmo.gitPush(repo = rp)
        
        # (2) Add new administrator
        elif choice == 2:
            prompt = 'Please give new administrator\'s GitHub id: '
            ghid = input(prompt).strip
            gro.addAdmin(github_id = ghid)
            
        # (3) Clone repositories
        elif choice == 3:
            gro.getRepos()
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

            for k,v in gro.org.repos.items():
                repo = os.path.join(cdir, k)
                remote = '{}{}/{}.git'.format(__rb, gro.org.name, k)
                lmo.gitClone(repo = repo, remote = remote)

        # (4) Update student remote repositories with local master
        elif choice == 4:
            gro.getRepos()

            while True:
                prompt = 'Please enter commit message: '
                mess = input(prompt).strip()
                print('\n{}\n'.format(mess))
                prompt = 'Is this okay or do you want to try again?'
                choice = pickOpt(prompt, ['Good', 'Try again'])
                if choice == 0:
                    break

            for k,v in gro.org.repos.items():
                repo = k
                repo_path = os.path.join(lmo.student_repo_dir, repo)
                if not os.path.isdir(repo):
                    continue
                lmo.gitPull(repo = repo_path)
                lmo.masterToStudent(student_repo = repo)
                lmo.gitAdd(repo = repo_path)
                lmo.gitCommit(repo = repo_path, message = mess)
                lmo.gitPush(repo = repo_path)                
            
        # (5) Pull down from remote student repositories
        elif choice == 5:
            gro.getRepos()

            prompt = 'Please select the student repository you wish to pull'
            opts = ['-- All student repositories --']
            for k,v in gro.org.repos.items():
                repo = os.path.join(lmo.student_repo_dir, k)
                if not os.path.isdir(repo):
                    continue
                opts.append(k)

            choice = pickOpt(prompt, opts)
            if choice == 0:
                for k,v in gro.org.repos.items():
                    repo_path = os.path.join(lmo.student_repo_dir, k)
                    if not os.path.isdir(repo_path):
                        continue
                    lmo.gitPull(repo = repo_path)
            else:
                repo_path = os.path.join(lmo.student_repo_dir, opts[choice])
                lmo.gitPull(repo = repo_path)

        # (6) Push from local student repository to remote
        elif choice == 6:
            gro.getRepos()

            prompt = 'Please select the student repository you wish to push'
            opts = ['-- All student repositories --']
            for k,v in gro.org.repos.items():
                repo = os.path.join(lmo.student_repo_dir, k)
                if not os.path.isdir(repo):
                    continue
                opts.append(k)

            while True:
                prompt = 'Please enter commit message: '
                mess = input(prompt).strip()
                print('\n{}\n'.format(mess))
                prompt = 'Is this okay or do you want to try again?'
                choice = pickOpt(prompt, ['Good', 'Try again'])
                if choice == 0:
                    break

            choice = pickOpt(prompt, opts)
            if choice == 0:
                for k,v in gro.org.repos.items():
                    repo_path = os.path.join(lmo.student_repo_dir, k)
                    if not os.path.isdir(repo_path):
                        continue
                    lmo.gitPull(repo = repo_path)
                    lmo.gitAdd(repo = repo_path)
                    lmo.gitCommit(repo = repo_path, message = mess)
                    lmo.gitPush(repo = repo_path)
            else:
                repo_path = os.path.join(lmo.student_repo_dir, opts[choice])
                lmo.gitPull(repo = repo)
                lmo.gitPull(repo = repo_path)
                lmo.gitAdd(repo = repo_path)
                lmo.gitCommit(repo = repo_path, message = mess)
                lmo.gitPush(repo = repo_path)

        # (7) Grade student assignments
        else:
            pass

        prompt = 'Do you have other tasks or wish to exit GitRoom Manager?'
        choice = pickOpt(prompt, ['I have another task', 'Exit'])

        if choice == 0:
            continue
        else:
            break

    print(closeout)
