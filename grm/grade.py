# grade.py                       
# -*- coding: utf-8 -*-

from .utils import *
from .api import *
from .loc import *
from .gr import *

import os
import textwrap
import sys

class Grader:

    __exitMessage = '\nLeaving grader and returning to GitRoom Manager...'

    def __init__(self, lgo):
        self.lgo = lgo
        self.grader = None

    def _listDir(self, pwdir):
        dir_list = []
        for f in os.listdir(pwdir):
            if not f.startswith('.'):
                dir_list.append(f)
        return dir_list

    def _chooseDorF(self, pwdir, dir_list):
        prompt = 'Please choose a file or directory'
        opts = ['-+- Top student repo directory -+-', '..']
        opts += dir_list
        opts += ['<< Exit grader >>']
        choice = pickOpt(prompt, opts)
        if choice == 0:
            return self.lgo.student_repo_dir
        elif choice == 1:
            return os.path.dirname(pwdir)
        elif choice == len(opts) - 1:
            return 0
        else:
            return os.path.join(pwdir, opts[choice])

    def _selectGrader(self):
        self.grader = input('Please give grader\'s name or initials: ').strip()

    def _commentFile(self):
        promptMessage('Add comments for end of file (hit return when finished)')
        com = textwrap.dedent(input('Comment:\n\n')).strip()
        com = textwrap.fill(com, width = 70)
        com = com.splitlines()
        comment_char = input('Please enter comment character (enter for none): ')
        comment = []
        for line in com:
            comment.append('{} '.format(comment_char) + line)
        comment = '\n'.join(comment)
        header = '\n\n{} COMMENTS from {}\n\n'.format(comment_char, self.grader)
        return header + comment
    
    def _gradeFile(self, file_to_grade):
        with open(file_to_grade, 'r') as f:
            print('-' * 34 + ' BEGIN FILE ' + '-' * 34)
            print(f.read())
            print('-' * 35 + ' END FILE ' + '-' * 35)

        comments = self._commentFile()

        with open(file_to_grade, 'a') as f:
            f.write(comments)

    def _choiceFlow(self, pwdir):
        choice = self._chooseDorF(pwdir, self._listDir(pwdir))
        if choice == 0:
            return self._quitGrader()
        elif os.path.isdir(choice):
            self._choiceFlow(choice)
        else:
            self._gradeFile(choice)

    def _quitGrader(self):
        print(self.__exitMessage)
        return 0

    def main(self):
        self._selectGrader()
        status = self._choiceFlow(self.lgo.student_repo_dir)

        if status != 0:
                   
            prompt = 'Would you like to grade another?'
            choice = pickOpt(prompt, ['Yes','No'])
            if choice == 0:
                self._choiceFlow(os.path.dirname(file_to_grade))
            else:
                self._quitGrader()
            

