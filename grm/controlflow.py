# controlflow.py
# -*- coding: utf-8 -*-

import json
import os
import subprocess as sp

from .utils import *
from .api import *
from .sys import *

def main():

    def initCourse(github_login = None, orgname = None, rostpath = None):
        gitroom = RemoteGit()
        gitroom.set_api_creds(ghid = github_login)
        gitroom.set_org(name = orgname)
        gitroom.build_roster(roster = rostpath)
        return gitroom

    def storeCourseInfo(courseobj):
        prompt = 'Do you want to store course information in JSON file?'
        choice = pickOpt(prompt, ['Yes','No'])

        if choice == 0:
            while True:
                prompt = 'Please give directory for saving: '
                odir = input(str(prompt)).strip()
                
                try:
                    odir = os.path.expanduser(odir)

                except AttributeError:
                    errorMessage('Please input a directory path')
                    continue

                info = {'github_login' : courseobj.admin.ghid,
                        'organization_name' : courseobj.org.name,
                        'roster_file'  : courseobj.roster.path}

                with open(odir + '/' + courseobj.org.name
                          + '_gitroom_info.json', 'w') as f:
                    json.dump(info, f, indent = 4)

                break

    def readCourseInfo(course_object_path):
        with open(course_object_path, 'r') as f:
            info = json.load(f)

        initCourse(github_login = info['github_login'],
                   orgname = info['organization_name'],
                   rostpath = info['rostpath'])

        
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

        # get GitRoom information
        gitroom = RemoteGit()
        gitroom.set_api_creds()
        gitroom.set_org()

        # (0) Initialize class
        if choice == 0:
            
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
