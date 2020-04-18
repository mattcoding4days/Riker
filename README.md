# Riker

## A command line C++ project generator written in Python, For shell dwelling Vimmers whom hate IDE's but still want to automate project generation

## Current Implemented features
    - [x] Creates a Library style console project (Easily modifiable)
    - [x] Creates Project heiarchy (src, hdr, man1, doc, tests, make_scripts)
    - [x] Creates an advanced flexible Makefile with support scripts
    - [x] builds and links hpp and cpp files out of the box
    - [x] Example man page
    - [x] Gives option to init project with git
    - [x] unicode and emoji support, and sweet Ansi escape colors (as every good CLI should have)

## What will the feature bring (hopefully)
    - [x] Generate Gtkmm projects (Gtk+)
    - [x] Generate Boost Lib projects
    - [x] Generate Ncurses projects
    - [x] Generate X11/X projects
    - [x] Each project should have simple tests already set up and running
    - [x] Give option to integrate Doxygen into each project
    - [x] Specificy C++ versioning

## Installation Process

* I have tried to automate the installation process, and make it as simple as possible
    - First, everything is ran through the make file.
    - install.py handles all the dirty work
    - DO NOT run install.py directly, it is called indirectly by make
    - Riker uses pyinstaller to compile the project to bytecode and install
    - The virtual env is activated, pip installs 3rd party modules from requirments.txt from the Makefile

### Riker supports Unicode, You will need a patched Nerdfont to see all the fancy symbols
[Here is a link to a nice Nerdfont](https://github.com/ryanoasis/nerd-fonts/blob/master/patched-fonts/SourceCodePro/Regular/complete/Sauce%20Code%20Pro%20Nerd%20Font%20Complete.ttf)
> Click on the 'view raw' button, your system will automatically download it, install the font,
> and enable it in your terminal of choice. Note: Gnome-terminal may require you to set the font in 
> sustem settings, not in the terminal font preferences, but try both methods.

```bash

# first things first... Get dependencies

# make sure you have pip installed (pythons package manager), or pip3 for non Arch users
# here is an example how to install pip3 on Ubuntu
sudo apt install python3-pip

# if you dont have your c/c++ installed you will need those
sudo apt install build-essential


# Clone the project
git clone https://github.com/mattcoding4days/Riker.git

# cd into Riker
make

# once make finishes it will have installed riker_run to /usr/local/bin
# thats it, now refresh your terminal and run
riker_run

# other make commands

# update the project
make update

# uninstall the project
make uninstall

# clean the project
make clean
```

## Usage

> Right now it is simple, no flags are impleneted, simply run 'riker_run'
> you will be prompted to enter the desired name of your project.
> Then you will be asked if you want to init a git repo. (currently not working).
> Riker will make the project in the directory that you are in when you run the program
>
> Please Note that Riker has been made to my own specifications and needs, it is for Linux development
> only Make as a build system is supported, Riker revolved around the specifications of my University
