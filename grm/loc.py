# loc.py
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
            master_repo = os.path.expanduser(master_repo).rstrip('/')
        if student_repo_dir:
            student_repo_dir = os.path.expanduser(student_repo_dir).rstrip('/')
        self.master_repo = master_repo
        self.student_repo_dir = student_repo_dir

    def __str__(self):
        text = 'Local master repo: {}\n'.format(self.master_repo)
        text += 'Local student repo directory: {}'.format(self.student_repo_dir)
        return text

    def set_master_repo(self, master_repo = None):
        if master_repo:
            self.master_repo = master_repo.rstrip('/')
            return

        while True:
            prompt = 'Please give path to course master repository: '
            mrp = input(str(prompt)).strip()
            try:
                mrp = os.path.expanduser(mrp)
            
            except AttributeError:
                errorMessage('Please input a proper path.')
                continue

            self.master_repo = mrp.rstrip('/')
            return

    def set_student_repo_dir(self, student_repo_dir = None):
        if student_repo_dir:
            self.student_repo_dir = student_repo_dir.rstrip('/')
            return

        while True:
            prompt = 'Please give path to student repository directory: '
            srdp = input(str(prompt)).strip()
            try:
                srdp = os.path.expanduser(srdp)
                    
            except AttributeError:
                errorMessage('Please input a proper path.')
                continue

            self.student_repo_dir = srdp.rstrip('/')
            return          
                
    # ----------------------------------
    # Git processes
    # ----------------------------------

    def gitInit(self, repo):
        args = ["git", "-C", repo, "init"]
        bequiet = sp.run(args)
        bequiet = None

    def gitRemoteAdd(self, repo, remote, remote_name = 'origin'):
        args = ["git", "-C", repo, "remote", "add", remote_name, remote]
        bequiet = sp.run(args)
        bequiet = None
    
    def gitClone(self, repo, remote):
        args = ["git", "clone", remote, repo]
        bequiet = sp.run(args)
        bequiet = None

    def gitPull(self, repo):
        args = ["git", "-C", repo, "pull"]
        bequiet = sp.run(args)
        bequiet = None

    def gitPush(self, repo, remote_name = 'origin', local_branch = 'master'):
        args = ["git", "-C", repo, "push", "-u", remote_name, local_branch]
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

    def createLocalRepo(self, student_repo):
        try:
            os.mkdir(os.path.join(self.student_repo_dir, student_repo))
        except FileExistsError:
            pass

    def masterToStudent(self, student_repo):
        args = ["rsync", "-r",
                "--exclude", "_*",  # protected directories
                "--exclude", ".*",  # ignore hidden dot files
                "--exclude", ".*/", # ignore hidden dot directories
                self.master_repo + "/",
                os.path.join(self.student_repo_dir, student_repo)]
        bequiet = sp.run(args)
        bequiet = None
        

