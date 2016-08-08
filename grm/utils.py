# utils.py
# -*- coding: utf-8 -*-

import sys

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
