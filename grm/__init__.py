# __init__.py
# -*- coding: utf-8 -*-

from .__info__ import __version__, __au, __dc, __rp

from .gr import *
from .api import *
from .loc import *
from .img import *
from .grade import *
from .utils import *

def main():

    connect_code = 1

    def __menu(cc):

        # update GitRoom Objects if cycling through program
        connect_code = gr.getGitRoomObjs(cc)

        # main prompt
        prompt = 'What would you like to do?'

        fullopts = ['Initialize class',
                    'Add students to class',
                    'Add new administrator',
                    'Clone repositories',
                    'Update student remote repositories with local main',
                    'Pull down from remote student repositories',
                    'Push from local student repositories to remotes',
                    'Grade student assignments',
                    '<< Exit Program >>']

        shortopts = [fullopts[i] for i in [len(fullopts) - 2, len(fullopts) - 1]]

        opts = shortopts if connect_code != 0 else fullopts
                       
        choice = pickOpt(prompt, opts)

        # exit program
        if choice == len(opts) - 1:
            return

        if connect_code != 0:
            choice += len(fullopts) - len(shortopts)
                             
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

        # (5) Update student remote repositories with local main
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
            if connect_code == 0:
                prompt = 'Do you want to push comments to student remotes?'
                choice = pickOpt(prompt, ['Yes','No'])
                if choice == 0:
                    gr.pushGR()

        prompt = 'Do you have other tasks or wish to exit GitRoom Manager?'
        choice = pickOpt(prompt, ['I have another task', 'Exit'])

        if choice == 0:
            __menu(connect_code)

    # ----------------------------------        
    # Run
    # ----------------------------------

    print(startup.format(__version__, __au, __dc, __rp))

    comp = Completer()
    # we want to treat '/' as part of a word, so override the delimiters
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(comp.pathCompleter)

    gr = GR()
    __menu(connect_code)
    progExit()
