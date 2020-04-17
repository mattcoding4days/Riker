'''
Arb Doc
'''
#!/usr/bin/env python3

import os
import sys
from colors import Colors as c
from riker import Riker
import templates


def get_project_input() -> str:
    '''
    get user input for name of project
    '''
    project_name = input(f"{c.BGreen}Enter name of project{c.Reset}: ")
    return project_name




def main():
    '''
    init the main routine

    '''
    proj_name = get_project_input()
    skeleton = Riker(proj_name)

    path = os.getcwd()
    new_path = os.path.join(path, proj_name)

    if not os.path.exists(new_path):
        os.mkdir(new_path)
    else:
        print('The path already exists')
        sys.exit(1)


    os.chdir(new_path)
    for directoy in skeleton.directories:
        os.mkdir(directoy)




if __name__ == '__main__':
    main()
