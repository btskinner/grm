# __init__.py
# -*- coding: utf-8 -*-

version = '0.1.0'

from .gr import *
from .api import *
from .sys import *
from .img import *
from .grade import *
from .utils import *

def main():

    def __progExit():
        print(closeout)
        sys.exit()

    def __menu():

        prompt = 'What would you like to do?'
        opts = ['Initialize class',
                'Add students to class',
                'Add new administrator',
                'Clone repositories',
                'Update student remote repositories with local master',
                'Pull down from remote student repositories',
                'Push from local student repositories to remotes',
                'Grade student assignments',
                '<< Exit Program >>']
        choice = pickOpt(prompt, opts)

        # exit program
        if choice == len(opts) - 1:
            return

        # update GitRoom Objects if cycling through program
        gr.getGitRoomObjs()
                             
        # (1) Initialize class
        if choice == 0:

            gr.buildGR(from_scratch = True)

        # (2) Add students to class
        elif choice == 1:
            
            gr.buildGR()
        
        # (3) Add new administrator
        elif choice == 2:

            gr.addGRAdmin()
            
        # (4) Clone repositories
        elif choice == 3:

            gr.cloneGR()

        # (5) Update student remote repositories with local master
        elif choice == 4:

            gr.updateGR()
            
        # (6) Pull down from remote student repositories
        elif choice == 5:

            gr.pullGR()

        # (7) Push from local student repository to remote
        elif choice == 6:

            gr.pushGR()

        # (8) Grade student assignments
        else:
            grader = Grader(gr.lgo)
            grader.main()

        prompt = 'Do you have other tasks or wish to exit GitRoom Manager?'
        choice = pickOpt(prompt, ['I have another task', 'Exit'])

        if choice == 0:
            __menu()

    # ----------------------------------        
    # Run
    # ----------------------------------

    print(startup.format(version))
    gr = GR()
    __menu()
    __progExit()
