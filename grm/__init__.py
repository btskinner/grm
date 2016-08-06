# __init__.py
# -*- coding: utf-8 -*-

version = '0.1.0'

from .api import Admin, Org, Student, Repository, Roster, Team, RemoteGit
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
        
        info = {'github_login' : gro.admin.ghid,
                'github_token_file' : gro.admin.token_file,
                'organization_name' : gro.org.name,
                'roster_file' : gro.roster.path,
                'master_repo' : lmo.master_repo,
                'student_repo_dir' : lmo.student_repo_dir}
        
        with open(odir + '/' + gro.org.name + '_gitroom_info.json', 'w') as f:
            json.dump(info, f, indent = 4)
            
        break

def initGitRoom(github_login = None, token_file = None, orgname = None,
                roster_file = None, master_repo = None,
                student_repo_dir = None):

    # GitRoom object
    gro = RemoteGit()
    gro.set_api_creds(ghid = github_login, tokenfile = token_file)
    gro.set_org(name = orgname)
    gro.build_roster(roster = roster_file)

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
            
    while True:
        # starting menu
        prompt = 'What would you like to do?'
        opts = ['Initialize class',
                'Add students to class',
                'Clone repositories',
                'Pull down from remote',
                'Update student repositories',
                'Grade student assignments']
        choice = pickOpt(prompt, opts)
 
        # (0) Initialize class
        if choice == 0:
            gro, lmo = getGitRoomObjs(gro, lmo)
        # (1) Add students to class
        elif choice == 1:
            pass
        # (2) Clone repositories
        elif choice == 2:
            pass
        # (3) Pull down from remote
        elif choice == 3:
            pass
        # (4) Update student repositories
        elif choice == 4:
            pass
        # (5) Grade student assignments
        else:
            pass

        prompt = 'Do you have other tasks or wish to exit?'
        choice = pickOpt(prompt, ['I have another task', 'Exit'])

        if choice == 0:
            continue
        else:
            break
