# utils.py
# -*- coding: utf-8 -*-

import os
import sys
import readline
import glob

# tab completer h/t https://gist.github.com/iamatypeofwalrus/5637895
class Completer(object):
    """ 
    A tab completer that can either complete from
    the filesystem or from a list.
    
    Partially taken from:
    http://stackoverflow.com/questions/5637124/tab-completion-in-pythons-raw-input
    """

    def pathCompleter(self, text, state):
        """ 
        This is the tab completer for systems paths.
        Only tested on *nix systems
        """
        line = readline.get_line_buffer().split()
        
        # replace ~ with the user's home dir.
        if '~' in text:
            text = os.path.expanduser('~')
            
        # autocomplete directories with having a trailing slash
        if os.path.isdir(text):
            text += '/'
                
        return [x for x in glob.glob(text + '*')][state]

def printOpts(optlist):
    for l in optlist:
        print('(', optlist.index(l) + 1, ')', l)

def promptMessage(text, char = '-'):
    print('\n')
    print(char * len(text))
    print(text)
    print(char * len(text), end = '\n\n')

def errorMessage(text):
    print('\n')
    print('ERROR: ', end = '')
    print(text, end = '\n\n')

def pickOpt(prompt, optlist):

    em1 = 'Only digits are accepted. Please choose again.'
    em2 = 'Please choose again from among the options.'

    while True:
        promptMessage(prompt)
        printOpts(optlist)
        try:
            choice = int(input('\nCHOICE: '))

        except ValueError:
            errorMessage(em1)
            continue

        except EOFError:
            print('\n')
            raise SystemExit

        if choice > len(optlist) or choice < 1:
            errorMessage(em2)
            continue

        return choice - 1

def progExit():
    print('\n\n{}{}{}\n\n'.format('-' * 28,' Exit GitRoom Manager ', '-' * 28))
    sys.exit()
