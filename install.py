'''
Installer script for the Riker C++ project generator
'''
#!/bin/env python3

import os
import shutil
import sys
import subprocess


# constants
BUILD_ENV = 'build_env'
INSTALL_DIR = '/usr/local/bin/'


def report_error(msg: str):
    '''
    central function for error reporting
    Print error msg to stderr, then exit
    '''
    sys.stderr.write(f'\n\n{msg}\n')
    sys.exit(1)


def check_permissions():
    '''
    check to see if user is running as root
    '''
    if not os.geteuid() == 0:
        report_error('Riker installer script requires root')


def exec_pyinstaller(build_path: str) -> str:
    '''
    call pyinstaller from subprocess
    and build this tasty project.
    returns the full path to the riker_run
    byte code binary
    '''
    # change to our new directory
    os.chdir(build_path)
    retval = subprocess.call("pyinstaller --onefile ../modules/riker_run.py", shell=True)
    if retval == 0:
        binary_path = os.path.join(build_path, 'dist')
        return binary_path

    # if we return empty string, install failed
    return ""


def install_executable(binary_path: str) -> bool:
    '''
    install the actual binary to
    /usr/local/bin
    '''
    success = None
    os.chdir(binary_path)
    retval = ''
    try:
        retval = shutil.move('riker_run', INSTALL_DIR)
    except shutil.Error as err:
        report_error(f'Not re-installing -> {err}')

    if os.path.isfile(retval):
        print(f"\nInstall successfull -> {retval}")
        success = True
        return success

    # install failed, return success as None
    return success


def clean_environment(project_root: str, build_env: str):
    '''
    clean up our build environment
    '''
    print(f'Cleaning environment -> {build_env}')
    os.chdir(project_root)
    try:
        shutil.rmtree(build_env)
    except OSError:
        report_error(f"Failed removing {build_env}")


def main():
    '''
    Main routine
    '''
    # check to see if user is root, if not return
    # informative error msg, and sys.exit
    check_permissions()

    # create a clean build environment directory for pyinstaller compile into
    riker_project_root = os.getcwd()
    build_environment = os.path.join(riker_project_root, BUILD_ENV)
    if not os.path.exists(build_environment):
        os.mkdir(build_environment)
    else:
        try:
            shutil.rmtree(build_environment)
            report_error('Build directory already exits, re-run the script')
        except OSError as err:
            report_error(f"{err}")

    # run pyinstaller and compile to bytecode
    bin_path = exec_pyinstaller(build_environment)

    # install executable to accessible $PATH
    if bin_path:
        retval = install_executable(bin_path)

        # clean up the installer scripts mess
        if retval:
            clean_environment(riker_project_root, build_environment)

    else:
        report_error("Pyinstall failed.. exiting")



if __name__ == '__main__':
    main()
