'''
Riker is a simple C++ project generator
'''
#!/usr/bin/env python3

import os
import sys
from colors import Colors as c

class Riker:
    '''
    The Riker class will handle all the implementation
    details
    '''
    def __init__(self: object, p_templates: {}):
        self.m_templates = p_templates
        self.m_directories = ['hdr', 'src', 'make_scripts', 'tests', 'doc', 'man1']
        self.m_project_name = ""
        self.m_initial_path = os.getcwd()
        self.m_full_project_path = ""
        self.m_git_repo = None

    @property
    def templates(self: object) -> {}:
        '''
        getter for templates hash map
        '''
        return self.m_templates

    @property
    def directories(self: object) -> []:
        '''
        return the list of directories
        that will build the project skeleton
        '''
        return self.m_directories

    @directories.setter
    def directories(self, new_dir: str):
        '''
        incase we want to make our project more complex
        we can add more directores to the list
        '''
        exists = None
        for folder in self.m_directories:
            if folder == new_dir:
                exists = True

        if not exists:
            self.m_directories.append(new_dir)
        else:
            print(f"{new_dir} already found in project list, did not add")

    @property
    def project_name(self: object) -> str:
        '''
        getter for project name
        '''
        return self.m_project_name

    @project_name.setter
    def project_name(self: object, p_project_name: str):
        '''
        setter for project name
        '''
        if not p_project_name:
            self.m_project_name = p_project_name
        else:
            print(f"{c.BRed}{p_project_name}{c.Reset} is empty.. Exiting")
            sys.exit(1)

    @property
    def initial_path(self: object) -> str:
        '''
        getter for path
        '''
        return self.m_initial_path

    @property
    def full_project_path(self: object) -> str:
        '''
        getter for the full/final project path
        '''
        return self.m_full_project_path

    @full_project_path.setter
    def full_project_path(self: object, p_full_project_path):
        '''
        setter for the full/final project path
        '''
        if not p_full_project_path:
            self.m_full_project_path = p_full_project_path
        else:
            print(f"{c.BRed}Project path cannot be empty{c.Reset}.. exiting")
            sys.exit(1)

    @property
    def git_repo(self: object) -> bool:
        '''
        getter for git repo
        '''
        return self.m_git_repo

    @git_repo.setter
    def git_repo(self: object, p_git_repo: bool):
        '''
        setter for git repo
        '''
        self.m_git_repo = p_git_repo

    def print_templates(self: object):
        '''
        Debug method: Print the contents of
        the templates hash map
        '''
        for key, value in self.templates.items():
            print(f"Key: {key},\n{value}")

    def get_user_input(self: object):
        '''
        Get user input for project name and git repo
        '''
        self.project_name = input(f"{c.BGreen}Enter project name:{c.Reset} ")

        valid = False
        while not valid:
            make_repo = input(f"{c.BGreen}Initialize the project with a git repo?:"
                              f"{c.Reset}{c.BBlue}[y/n]{c.Reset} ").lower()

            if make_repo in ('y', 'yes'):
                self.m_git_repo = True
                valid = True
            elif make_repo in ('n', 'no'):
                self.m_git_repo = False
                valid = True
            else:
                print(f"{c.BYellow}Expected yes or no{c.Reset}")

    def build_project(self: object):
        '''
        This is the project builder method
        '''
        self.full_project_path = os.path.join(self.initial_path, self.project_name)
        if not os.path.exists(self.full_project_path):
            os.mkdir(self.full_project_path)
        else:
            print(f"{c.BYellow}{self.full_project_path}{c.Reset} already exists\n"
                  f"exiting...")
            sys.exit(1)
        # change to the new directory
        os.chdir(self.full_project_path)
        # create all the directories
        for directory in self.directories:
            print(f"{c.BBlue}   {c.Reset} Creating {directory}")
            os.mkdir(directory)
