'''
Arb Doc
'''
#!/usr/bin/env python3

from riker import Riker
from templates import TEMPLATES


def main():
    '''
    init the main routine

    '''
    riker = Riker(TEMPLATES)
    riker.get_user_input()
    riker.build_directories()
    riker.build_project()



if __name__ == '__main__':
    main()
