# Author: Nathaniel Pawluk
# Course: ITSC204
# Description: Conversion of ARM toolchain to python from bash

import os, sys, re

if len(sys.argv) == 1:  #If no arguments are given, display the user guide
    print("Usage:\n")
    print("arm_toolchain.py [-p | --port <port number, default 12222>] <assembly filename> [-o | --output <output filename>]\n")
    print("-v | --verbose               Show some information about steps performed.")
    print("-g | --gdb                   Run gdb command on executable.")
    print("-b | --break <break point>   Add breakpoint after running gdb. Default is _start.")
    print("-r | --run                   Run program in gdb automatically. Same as run command inside gdb env.")
    print("-q | --qemu                  Run executable in QEMU emulator. This will execute the program.")
    print("-p | --port                  Specify a port for communication between QEMU and GDB. Default is 12222.")
    print("-o | --output <filename>     Output filename.")

    sys.exit()  # Exit after printing the user guide

# Default arguments
GDB = False
OUTPUT_FILE = ""
VERBOSE = False
QEMU = False
PORT = "12222"
BREAK = "main"
RUN = False

# Looking for argument flags
for i in range(len(sys.argv)):
    arg = sys.argv[i]
    if arg == "-v" or arg == "--verbose":
        VERBOSE = True
    elif arg == "-g" or arg == "--gdb":
        GDB = True
    elif arg == "-b" or arg == "--break":
        BREAK = sys.argv[i+1]
    elif arg == "-r" or arg == "--run":
        RUN = True
    elif arg == "-q" or arg == "--qemu":
        QEMU = True
    elif arg == "-p" or arg == "--port":
        PORT = sys.argv[i+1]
    elif arg ==  "-o" or arg == "--output":
        OUTPUT_FILE = sys.argc[i+1]
    else: # Case for unrecognized flag
        if re.search("-.+", sys.argv[i]) or re.search("--.+", sys.argv[i]):
            print(f"Unknown option {sys.argv[i]}")
            sys.exit()

# Attempt to open the given file
try:
    INPUT_FILE = open(sys.argv[1], "r")
except:
    print(f"File {sys.argv[1]} does not exist!")
    sys.exit()

# If no output file name was given, strip .nasm and use that
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
    print(f"  Port = {PORT}\n")
    print("Compiling started...")

# Raspberry Pi 3B
os.system(f"arm-linux-gnueabihf-gcc -ggdb -mfpu=vfp -march=armv6+fp -mabi=aapcs-linux {sys.argv[1]} -o {OUTPUT_FILE} -static -nostdlib")

# Added output from VERBOSE
if VERBOSE == True:
    print("Compiling finished")

if QEMU == True and GDB == False:   #Only run QEMU
    print("Starting QEMU...\n")
    os.system(f"qemu-arm {OUTPUT_FILE}")
    sys.exit()

elif QEMU == False and GDB == True: #Run QEMU in remote and GDB with remote target
    print(f"Starting QEMU in Remote Mode listening on port {PORT}...")
    os.system(f"qemu-arm -g {PORT} {OUTPUT_FILE}")
    gdb_params = f"ex \"target remote 127.0.0.1:{PORT}\" -ex \"b {BREAK}\""

    if RUN == True:
        gdb_params += " -ex \"r\""
    
    print("Starting GDB in Remote Mode connecting to QEMU...")
    os.system(f"gdb-multiarch {gdb_params} {OUTPUT_FILE}")
    sys.exit()

elif QEMU == False and GDB == False:
    # Don't run QEMU or GDB and exit normally
    sys.exit()

else:
    # Error case. Display error and run QEMU afterwards
    print("\n****\n*\n* You can't use QEMU (-q) and GDB (-g) options at the same time.")
    print("* Defaulting to QEMU only.\n*\n****\n\nStarting QEMU...\n")
    os.system(f"qemu-arm {OUTPUT_FILE}")
    sys.exit()
