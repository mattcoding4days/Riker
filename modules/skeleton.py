'''
Riker is a simple C++ project generator
'''
#!/usr/bin/env python3

from colors import Colors
import os
import shutil
import templates


class Skeleton:
    '''
    Skeleton to handle templates for C++ project
    '''
    def __init__(self: object, p_project_name: str):
        self.m_project_name = p_project_name
        self.m_make = "Makefile"
        self.m_directories = ['hdr', 'src', 'make_scripts', 'tests', 'doc', 'man1']

    @property
    def project_name(self: object) -> str:
        '''
        getter for project name
        '''
        return self.m_project_name

    @property
    def makefile(self: object) -> str:
        '''
        return the makefile string
        '''
        return self.m_make

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
