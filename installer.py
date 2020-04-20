'''
Installer script for Riker
'''
#!/usr/bin/env python3

import argparse
import os
import shutil
import sys
import subprocess


# color constants
GRE = "\033[1;32m"
RED = "\033[1;31m"
YEL = "\033[1;33m"
BLU = "\033[1;34m"
RES = "\033[0m"


class Installer:
    '''
    Arb Doc
    '''
    def __init__(self, _build_dir='build-env', _install_dir='.bin',
                 _venv_dir='riker-env', _debug=False):

        self.riker_root = os.getcwd()
        self.user_home = os.path.expanduser('~/')
        self.build_environment = os.path.join(self.riker_root, _build_dir)
        self.install_dir = os.path.join(self.user_home, _install_dir)
        self.venv_dir = os.path.join(self.riker_root, _venv_dir)
        self.debug = _debug
        self.export_code = f'\n# Appended by Riker installer script\n' \
                           f'export PATH="$PATH:$HOME/{_install_dir}"'
        self.install_dir_exists = None



    def report_error(self: object, msg: str):
        '''
        centralized error reporting method
        '''
        sys.stderr.write(f'{RED}\n\n{msg} aborting install{RES}\n')
        self.clean()
        sys.exit(1)



    def __cd_project_root(self):
        '''
        ! Private method: Only to be used by public methods
        check to see the current working directory,
        if it does not match the projects root directory
        then change directory back to project root
        '''
        if not os.getcwd() == self.riker_root:
            if self.debug:
                print(f'{YEL}Debug: {self.__cd_project_root.__name__}'
                      f' -> changing back to project root from {os.getcwd()} {RES}')
            os.chdir(self.riker_root)



    def __write_profile(self: object):
        '''
        ! Private method: Only to be used by public methods
        append export code to users .profile
        '''
        os.chdir(self.user_home)
        profile = '.profile'
        try:
            if os.path.isfile(profile):
                with open(profile, 'at') as file:
                    if self.debug:
                        print(f'{YEL}Debug: {self.__write_profile.__name__}'
                              f' -> Appending new path export to {profile} {RES}')
                    file.write(self.export_code)
                    file.close()
        except OSError as err:
            error = f"Error: {self.__write_profile.__name__} -> {err}"
            self.report_error(error)

        # go back to project root folder
        self.__cd_project_root()



    def prepare(self: object):
        '''
        check to see if ~/install_dir exists
        if not, create it, then
        '''
        if os.path.exists(self.install_dir):
            if self.debug:
                print(f'{YEL}Debug: {self.prepare.__name__}'
                      f' -> The path {self.install_dir} exists {RES}')
            self.install_dir_exists = True
        else:
            if self.debug:
                print(f'{YEL}Debug: {self.prepare.__name__}'
                      f' -> The path {self.install_dir} does not exist {RES}')

                print(f'{YEL}Debug: {self.prepare.__name__}'
                      f' -> Changing directory into {self.user_home} {RES}')


            os.mkdir(self.install_dir)
            self.install_dir_exists = True

            if self.debug:
                print(f'{YEL}Debug: {self.prepare.__name__}'
                      f' -> Making directory {self.install_dir} {RES}')

            # call helper method to write to .profile
            self.__write_profile()



    def __invoke_pip(self, full_run=True):
        '''
        ! Private method: Only to be used by public methods
        invoke a subprocess to run pip3
        '''
        venv = os.path.basename(self.venv_dir)
        try:
            if full_run:
                subprocess.call(f'python3 -m venv {venv}', shell=True)
                # check and see if pip needs to be upgraded first
                subprocess.call(f'./{venv}/bin/pip3 install --upgrade pip', shell=True)
                subprocess.call(f'./{venv}/bin/pip3 install -r requirements.txt', shell=True)
            else:
                subprocess.call(f'./{venv}/bin/pip3 install -r requirements.txt', shell=True)
        except OSError as err:
            error = f"Error: {self.__invoke_pip.__name__} -> {err}"
            self.report_error(error)



    def __prepare_virtual_env(self: object):
        '''
        ! Private method: Only to be used by public methods
        1. Create the virtual env from this script
        2. use pip3 from installed virtual environment
           ( a work around so we dont have to source the ghetto activate script
           install from the requirements file
        '''
        # make sure we are in project root folder
        self.__cd_project_root()
        if not os.path.exists(self.venv_dir):
            require = 'requirements.txt'
            if not os.path.exists(require):
                self.report_error(f'Cannont find {require}')

            if self.debug:
                print(f'{YEL}Debug: {self.__prepare_virtual_env.__name__}'
                      f' -> {require} exists {RES}')
                print(f'{YEL}Debug: {self.__prepare_virtual_env.__name__}'
                      f' -> {self.venv_dir} does not exist, preparing 3 subprocess calls {RES}')

            # run pip3 package manager
            self.__invoke_pip()

        else:
            if self.debug:
                print(f'{YEL}Debug: {self.__prepare_virtual_env.__name__}'
                      f' -> {self.venv_dir} exists, checking if riker_run is installed {RES}')

            riker = self.install_dir + '/riker_run'
            if os.path.exists(riker):
                self.report_error(f'riker_run is already installed at {riker}')
            else:
                if self.debug:
                    print(f'{YEL}Debug: {self.__prepare_virtual_env.__name__}'
                          f' -> {riker} is not installed, preparing 1 subprocess calls {RES}')

                # run pip3 package manager
                self.__invoke_pip(False)



    def build(self: object):
        '''
        call __prepare_virtual_env
        Create a clean build env folder in Riker project root
        run pyinstaller and compile riker_run and dependencies into
        a singlye byte code executable

        '''
        # first make sure the virtual env is set up,
        # and our 3rd party tools are installed
        self.__prepare_virtual_env()

        # make build environment
        self.__cd_project_root()
        if not os.path.exists(self.build_environment):
            if self.debug:
                print(f'{YEL}Debug: {self.build.__name__}'
                      f' -> creating {self.build_environment} directory {RES}')
            os.mkdir(self.build_environment)

        # execute the pyinstaller
        os.chdir(self.build_environment)
        try:
            if self.debug:
                print(f'{YEL}Debug: {self.build.__name__}'
                      f' -> preparing to run a subprocess in {os.getcwd()} {RES}')
            venv = os.path.basename(self.venv_dir)
            subprocess.call(f'../{venv}/bin/pyinstaller --onefile ../modules/riker_run.py',
                            shell=True)

        except OSError as err:
            error = f"Error: {self.build.__name__} -> {err}"
            self.report_error(error)



    def install(self: object):
        '''
        move the riker_run executable from dist folder to
        self.install_dir
        '''
        riker_binary = os.path.join(self.build_environment, 'dist')
        is_installed = ''
        try:
            os.chdir(riker_binary)
            if self.debug:
                print(f'{YEL}Debug: {self.install.__name__}'
                      f' -> preparing to run a subprocess in {os.getcwd()} {RES}')

            is_installed = shutil.move('riker_run', self.install_dir)
        except OSError as err:
            error = f"Error: {self.install.__name__} -> {err}"
            self.report_error(error)

        if is_installed:
            print(f'\n{GRE}Install has been successfull -> {is_installed} {RES}'
                  f'\n{BLU}Please logout and log back in {RES}\n')



    def clean(self: object):
        '''
        clean the virtual environment and build env
        '''
        try:
            os.chdir(self.riker_root)
            if os.path.exists(self.venv_dir):
                venv = os.path.basename(self.venv_dir)
                if self.debug:
                    print(f'{YEL}Debug: {self.clean.__name__}'
                          f' -> Removing {venv} {RES}')
                shutil.rmtree(venv)

            if os.path.exists(self.build_environment):
                build = os.path.basename(self.build_environment)
                if self.debug:
                    print(f'{YEL}Debug: {self.clean.__name__}'
                          f' -> Removing {build} {RES}')
                shutil.rmtree(build)

        except OSError as err:
            error = f"Error: {self.clean.__name__} -> {err}"
            self.report_error(error)


def main():
    '''
    main routine
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="enable debug logging",
                        action="store_true")

    args = parser.parse_args()

    if args.debug:
        install = Installer(_debug=True)
    else:
        install = Installer()

    install.prepare()
    install.build()
    install.install()
    install.clean()

if __name__ == '__main__':
    main()
