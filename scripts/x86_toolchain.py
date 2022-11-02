# Author: Nathaniel Pawluk
# Course: ITSC204
# Description: Conversion of x86 toolchain to python from bash

import os, sys

if len(sys.argv) == 1:  #If no arguments are given, display the user guide
    print("Usage:\n")
    print("x86_toolchain.py [ options ] <assembly filename> [-o | --output <output filename>]\n")
    print("-v | --verbose               Show some information about steps performed.")
    print("-g | --gdb                   Run gdb command on executable.")
    print("-b | --break <break point>   Add breakpoint after running gdb. Default is _start.")
    print("-r | --run                   Run program in gdb automatically. Same as run command inside gdb env.")
    print("-q | --qemu                  Run executable in QEMU emulator. This will execute the program.")
    print("-32| --x86-32                Compile for 32bit (x86-32) system.")
    print("-o | --output <filename>     Output filename.")

    sys.exit()  #Exit after printing the user guide

#Default arguments
GDB = False
OUTPUT_FILE = ""
VERBOSE = False
BIT64 = True
QEMU = False
BREAK = "_start"
RUN = False

for i in range(len(sys.argv)): #Looking for argument flags
    match sys.argv[i]:
        case "-v" | "--verbose":
            VERBOSE = True
        case "-g" | "--gdb":
            GDB = True
        case "-b" | "--break":
            BREAK = sys.argv[i+1]
        case "-r" | "--run":
            RUN = True
        case "-q" | "--qemu":
            QEMU = True
        case "-32"| "--x86-32":
            BIT64 = False
        case "-o" | "--output":
            OUTPUT_FILE = sys.argc[i+1]

# Attempting to open the given file
try:
    INPUT_FILE = open(sys.argv[1], "r")
except:
    print(f"File {sys.argv[1]} does not exist!")
    sys.exit()

# If no output name is given, strip .nasm and use that
if OUTPUT_FILE == "":
    OUTPUT_FILE = sys.argv[1].strip(".nasm")

# Showing argument values if VERBOSE is true
if VERBOSE == True:
    print("Arguments being set:")
    print(f"  GDB = {GDB}")
    print(f"  RUN = {RUN}")
    print(f"  BREAK = {BREAK}")
    print(f"  QEMU = {QEMU}")
    print(f"  Input File = {sys.argv[1]}")
    print(f"  Output File = {OUTPUT_FILE}")
    print(f"  Verbose = {VERBOSE}")
    print(f"  64 bit mode = {BIT64}\n")
    print("NASM started...")

# Compile in 64 or 32 bit mode based on BIT64
if BIT64 == True:
    os.system(f"nasm -f elf64 {sys.argv[1]} -o {OUTPUT_FILE}.o")
else:
    os.system(f"nasm -f elf {sys.argv[1]} -o {OUTPUT_FILE}.o")

# Added output from VERBOSE
if VERBOSE == True:
    print("NASM finished\nLinking...")

#Linking
if BIT64 == True:
    os.system(f"ld -m elf_x86_64 {OUTPUT_FILE}.o -o {OUTPUT_FILE}")
else:
    os.system(f"ld -m elf_i386 {OUTPUT_FILE}.o -o {OUTPUT_FILE}")

# Added output for VERBOSE
if VERBOSE == True:
    print("Linking finished")

# Use QEMU if -q flag was given
if QEMU == True:
    print("Starting QEMU...\n")
    if BIT64 == True:
        os.system(f"qemu-x86_64 {OUTPUT_FILE}")
    else:
        os.system(f"qemu-i386 {OUTPUT_FILE}")
    sys.exit()
    
# Use GDB if -g flag was given
if GDB == True:
    gdb_params = f"-ex \"b {BREAK}\""
    if RUN == True:
        gdb_params += " -ex \"r\""
    os.system(f"gdb {gdb_params} {OUTPUT_FILE}")
