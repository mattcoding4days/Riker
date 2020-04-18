'''
Riker is a simple C++ project generator
'''
#!/usr/bin/env python3

import os
import sys
from constants import Colors as c
from constants import Devicons as icons


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
        if p_project_name:
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
        if p_full_project_path:
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


    def build_directories(self: object):
        '''
        set the proper full project path,
        cd into that path, iterate through the directories list
        and mkdir on each index.
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
        print('\n')
        for directory in self.directories:
            print(f"{c.BBlue}{icons.Folder}{c.Reset} Creating {c.BPurple}{directory}{c.Reset}")
            os.mkdir(directory)
        print("\n")


    def __build_helper(self: object, directory: str, file_match: str) -> str:
        '''
        Helper: TODO: Fill out later
        directory is an element in the directories list.
        '''
        temp_file = ""
        temp_path = ""

        # if directory string is empty
        if not directory:
            temp_path = self.full_project_path
        else:
            temp_path = os.path.join(self.full_project_path, directory)

        print(f"{c.BBlue}{icons.Open_Folder}{c.Reset}{c.BGreen} => {c.Reset}Entering {temp_path}")
        curr_path = os.getcwd()
        if curr_path != temp_path:
            os.chdir(temp_path)

        # get the proper file from the templates hash map
        for key, value in self.templates.items():
            if key == file_match:
                temp_file = value

        return temp_file


    @staticmethod
    def __write_files(temp_file: str, file_match: str) -> bool:
        '''
        write the corresponding files into given directory
        if the string that is holding the file is empty, return False,
        else return True
        '''
        success = None
        if temp_file:
            with open(file_match, 'xt') as file:
                print(f"\t{c.BBlue}{icons.Header}{c.Reset} Attempting to create {file_match}")
                file.write(temp_file)
            success = True

        return success


    @staticmethod
    def __is_success(value: bool, directory: str, file_match: str):
        '''
        evaluate if boolean value is True or False,
        print proper messsage
        '''
        if value:
            print(f"\t{c.BGreen}{icons.Success} Success{c.Reset} "
                  f"creating {file_match} in directory {directory}\n")
        else:
            print(f"\t{c.BRed}\t{icons.Failure} Failure{c.Reset} "
                  f"creating {file_match} in directory {directory}\n")


    def build_project(self: object):
        '''
        cd into each of those paths, and create the proper file.
        [eg] example.hpp -> hdr folder, example.cpp -> src folder
        '''
        # first create the Makefile in the project root
        file_match = 'Makefile'
        make_file = self.__build_helper("", file_match)
        retval = self.__write_files(make_file, file_match)
        self.__is_success(retval, os.path.basename(self.full_project_path), file_match)

        # cd into each new directory and create the files in the proper directory
        for directory in self.directories:
            # change to project root for the beginning
            # of each iteration
            curr_path = os.getcwd()
            if curr_path != self.full_project_path:
                os.chdir(self.full_project_path)

            temp_file = ""

            if directory in 'hdr':
                file_match = 'example.hpp'
                temp_file = self.__build_helper(directory, file_match)

                retval = self.__write_files(temp_file, file_match)
                self.__is_success(retval, directory, file_match)

            elif directory in 'src':
                file_match = 'example.cpp'
                temp_file = self.__build_helper(directory, file_match)

                retval = self.__write_files(temp_file, file_match)
                self.__is_success(retval, directory, file_match)

                # reset string, we have two files going in the src directory
                file_match = ""
                temp_file = ""

                file_match = 'main.cpp'
                temp_file = self.__build_helper(directory, file_match)

                retval = self.__write_files(temp_file, file_match)
                self.__is_success(retval, directory, file_match)
