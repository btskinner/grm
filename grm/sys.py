# sys.py
# -*- coding: utf-8 -*-

import os
import subprocess as sp

from .utils import *

class LocalGit:

    '''
    Class for local machine system management
    '''

    def __init__(self, master_repo = None, student_repo_dir = None):
        if master_repo:
            master_repo = os.path.expanduser(master_repo)
        if student_repo_dir:
            student_repo_dir = os.path.expanduser(student_repo_dir)
        self.master_repo = master_repo
        self.student_repo_dir = student_repo_dir

    def __str__(self):
        text = 'Local master repo: {}\n'.format(self.master_repo)
        text += 'Local student repo directory: {}'.format(self.student_repo_dir)
        return text

    def set_master_repo(self, master_repo = None):
        if master_repo:
            self.master_repo = master_repo
            return

        while True:
            prompt = 'Please give path to course master repository: '
            mrp = input(str(prompt)).strip()
            try:
                mrp = os.path.expanduser(mrp)
            
            except AttributeError:
                errorMessage('Please input a proper path.')
                continue

            self.master_repo = mrp
            return

    def set_student_repo_dir(self, student_repo_dir = None):
        if student_repo_dir:
            self.student_repo_dir = student_repo_dir
            return

        while True:
            prompt = 'Please give path to student repository directory: '
            srdp = input(str(prompt)).strip()
            try:
                srdp = os.path.expanduser(srdp)
                    
            except AttributeError:
                errorMessage('Please input a proper path.')
                continue

            self.student_repo_dir = srdp
            return          
                
    # ----------------------------------
    # Git processes
    # ----------------------------------

    def gitClone(self, student_git_url, student_repo_name):
        args = ["git", "clone", student_git_url,
                self.student_repo_dir + "/" + student_repo_name]
        bequiet = sp.run(args)
        bequiet = None

    def gitPull(self, repo):
        args = ["git", "-C", repo, "pull"]
        bequiet = sp.run(args)
        bequiet = None

    def gitPush(self, repo, remote_name, local_branch = 'master'):
        args = ["git", "-C", repo, "push", remote_name, local_branch]
        bequiet = sp.run(args)
        bequiet = None

    def gitAdd(self, repo):
        args = ["git", "-C", repo, "add", "."]
        bequiet = sp.run(args)
        bequiet = None

    def gitCommit(self, repo, message):
        args = ["git", "-C", repo, "commit", "-m", message]
        bequiet = sp.run(args)
        bequiet = None
  
    # ----------------------------------
    # Local system file copy processes
    # ----------------------------------

    def masterToStudent(self, student_repo):
        args = ["rsync", "-r", "--exclude", "_*",
                self.master_repo + "/", student_repo]
        bequiet = sp.run(args)
        bequiet = None
        

