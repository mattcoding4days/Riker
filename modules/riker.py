'''
Arb Doc
'''
#!/usr/bin/env python3

import os
from colors import Colors as c
import shutil
from skeleton import Skeleton
import templates


def get_project_input():
    '''
    get user input for name of project
    '''





def main():
    '''
    init the main routine

    '''
    current_path = os.getcwd()
    print(current_path)
    dirs_in_path = os.listdir()

    # iterate through the directories in the path
    # to make sure we have a match
    for item in dirs_in_path:
        if item == 'test':
            new_path = os.path.join(current_path, item)
            os.chdir(new_path)
            print(os.getcwd())





if __name__ == '__main__':
    main()