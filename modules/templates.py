'''
This file contains multiline interpolated strings
held in a dictionary
that represent generic C++, bash and makefile code
'''
#!/usr/bin/env python3


TEMPLATES = {
    # item 1 example.cpp
    'class_file' : f"""#include <iostream>
#include "../hdr/example.hpp"

/* Generated by Riker */

// default constructor
Example::Example(void)
  : m_private("This is the default constructor")
{{
  /*
   *Uneeded
   */
}}


// defined constructor
Example::Example(const std::string &p_private)
  : m_private(p_private)
{{
  /*
   *Uneeded
   */
}}


// destructor
Example::~Example(void)
{{
  /*
   *Uneeded
   */
}}


// copy constructor
Example::Example(const Example &src)
  :m_private(src.m_private)
{{
  /*
   *Uneeded
   */
}}


  // copy assignment
Example& Example::operator = (const Example &src)
{{
  if (this == &src) {{
    return *this;
  }}
  // init copy
  this->m_private = src.m_private;

  return *this;
}}


// move constructor
Example::Example(Example &&src) noexcept
  :m_private(src.m_private)
{{
  // reset original object
  this->m_private = "";
}}


// move assignment
Example& Example::operator = (Example &&src) noexcept
{{
  if (this == &src) {{
    return *this;
  }}

  // init move
  this->m_private = src.m_private;

  // reset original object because ownership has moved
  this->m_private = "";

  return *this;
}}


// overload the outstream operator
std::ostream& operator << (std::ostream& os, const Example& src)
{{
  os << "Private variable: " << src.getPrivate() << std::endl;
  return os;
}}


// getter for m_private
const std::string& Example::getPrivate(void) const {{ return this->m_private; }}


// setter for m_private
void Example::setPrivate(const std::string &p_private)
{{
  if (!p_private.empty()) {{
    this->m_private = p_private;
  }}
}}

""",

    # item 2 main.cpp
    'main_file' : f"""#include "../hdr/example.hpp"
#include <iostream>

/* Generated by Riker */

int main(void)
{{
  Example test("Defined Constructor");
  Example test_two;

  std::cout << test;
  std::cout << test_two;

  return 0;
}}

""",

    # item 3 example.hpp
    'header_file' : f"""#ifndef EXAMPLE_HPP
#define EXAMPLE_HPP

#include <string>

/* Generated by Riker */
//this implementation obeys the rule of seven

class Example
{{
  private:
    std::string m_private;
  public:
    // default constructor
    Example(void);

    // defined constructor
    Example(const std::string &p_private);

    // destructor
    ~Example(void);

    // copy constructor
    Example(const Example &src);

    // copy assignment
    Example& operator = (const Example &src);

    // move constructor
    Example(Example &&src) noexcept;

    // move assignment
    Example& operator = (Example &&src) noexcept;

    // overload the outstream operator
    friend std::ostream& operator << (std::ostream& os, const Example& src);

    // getter for m_private
    const std::string& getPrivate(void) const;

    // setter for m_private
    void setPrivate(const std::string &p_private);
}};

#endif

""",

    # item 4 Makefile
    'make_file' : f"""RELEASE=$(CXX) $(WARNINGS) $(OUT_FLG)
DEBUG=$(CXX) $(WARNINGS) $(DEBUG_FLG) $(OUT_FLG)
CXX=g++
DEBUG_FLG=-g
BUILD_FLG=-c
OUT_FLG=-o
WARNINGS=-Wall -Wextra
TARGET=bin/test
TARGET_DEBUG=bin/test_debug
OBJ_DIR=obj/
OBJ_DEBUG_DIR=objd/
OBJ_FILES=$(OBJ_DIR)*.o
OBJ_FILES_DEBUG=$(OBJ_DEBUG_DIR)*.o
VERSION=0.0.1

# Generated by Riker

all: $(TARGET) $(TARGET_DEBUG)

release: $(TARGET)

debug: $(TARGET_DEBUG)

$(TARGET): obj/example.o obj/main.o
	$(RELEASE) $(TARGET) $(OBJ_FILES)

$(TARGET_DEBUG): objd/example.o objd/main.o
	$(DEBUG) $(TARGET_DEBUG) $(OBJ_FILES_DEBUG)

# Release
# g++ -Wall -Wextra -c obj/example.o -o src/example.cpp
obj/example.o: src/example.cpp
	@echo
	@bash make_scripts/prelim_checks.sh -r
	@echo
	@echo "Building Release Version: $(VERSION)"
	@echo "============================="
	$(CXX) $(WARNINGS) $(BUILD_FLG) $< $(OUT_FLG) $@

# g++ -Wall -Wextra -c obj/main.o -o src/main.cpp
obj/main.o: src/main.cpp
	$(CXX) $(WARNINGS) $(BUILD_FLG) $< $(OUT_FLG) $@

# Debug
# g++ -Wall -Wextra -c obj/example.o -o src/example.cpp
objd/example.o: src/example.cpp
	@echo
	@bash make_scripts/prelim_checks.sh -d
	@echo
	@echo "Building Debug Version: $(VERSION)"
	@echo "============================="
	$(CXX) $(WARNINGS) $(BUILD_FLG) $(DEBUG_FLG) $< $(OUT_FLG) $@

# g++ -Wall -Wextra -c obj/main.o -o src/main.cpp
objd/main.o: src/main.cpp
	$(CXX) $(WARNINGS) $(BUILD_FLG) $(DEBUG_FLG) $< $(OUT_FLG) $@


clean:
	@bash make_scripts/clean_checks.sh

.PHONY: all release debug clean

""",

    #item 5 clean_checks.sh
    'clean_checks' : f"""#!/bin/bash

# Generated by Riker
# source our environment vars,

# need to source with full path since makefile will be calling it
source make_scripts/global_vars.sh

if [[ -d "$_OBJ" ]]; then
  printf "Removing Object Files Directory\\n"
  rm -rf "$_OBJ"
else
  printf "Nothing to do for ==> %s\\n" "$_OBJ"
fi

# check if debug object directory exits
if [[ -d "$_OBJD" ]]; then
  printf "Removing Object Files Debug Directory\\n"
  rm -rf "$_OBJD"
else
  printf "Nothing to do for ==> %s\\n" "$_OBJD"
fi

# check if binary directory exits
if [[ -d "$_BIN" ]]; then
  printf "Removing Binary Directory\\n"
  rm -rf "$_BIN"
else
  printf "Nothing to do for ==> %s\\n" "$_BIN"
fi

""",

    #item 6 prelim_checks.sh
    'prelim_checks' : f"""#!/bin/bash

# Generated by Riker
# This is a helper build script for the root project makefile
# A build rule will only be triggered if the script is called with
# either '-r' for release or '-d' for debug

# since the root makefile will be calling the scripts
# the path must be sourced from the makefiles position
# in the hiearchy
# NOTE: eg: makefile -> make_scripts/prelim_checks.sh

source make_scripts/global_vars.sh


function trigger_release() {{
  # check if object directory exists
  if [[ ! -d "$_OBJ" ]]; then
    printf "Creating Object Files Directory\\n"
    mkdir "$_OBJ"
  fi

  # check if binary directory exits
  trigger_binary
}}


function trigger_debug() {{
  # check if debug object directory exits
  if [[ ! -d "$_OBJD" ]]; then
    printf "Creating Object Debug Files Directory\\n"
    mkdir "$_OBJD"
  fi

  # check if binary directory exits
  trigger_binary
}}


function trigger_binary() {{
  # build the binary directory
  if [[ ! -d "$_BIN" ]]; then
    printf "Creating Binary Directory\\n"
    mkdir "$_BIN"
  fi
}}


# entry point
if [[ "$#" -eq 1 ]]; then
  for arg; do
    if [[ "$arg" == "-r" ]]; then
      trigger_release
    elif [[ "$arg" == "-d" ]]; then
      trigger_debug
    else
      printf "%s accepts only one Argument:\\n -r : release\\n-d : debug\\n" "$0"
    fi
  done
fi
""",

    # item 7 global_vars.sh
    'global_vars' : f"""#!/bin/bash

# Generated by Riker
# File for globally exported variables
# so make_scripts dont have to redeclare
_OBJ="obj"
_OBJD="objd"
_BIN="bin"

# export as environment variables for other scripts
export _OBJ
export _OBJD
export _BIN
"""
}
