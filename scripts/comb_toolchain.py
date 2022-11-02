# Author: Nathaniel Pawluk
# Course: ITSC204
# Description: Combining the x86 and arm toolchains

from curses.ascii import isdigit
import os, sys, re

if len(sys.argv) == 1:  # If no arguments are given, display the user guide
    print("Usage:\n")
    print("comb_toolchain.py <assembly filename> [ toolchain ] [ options ] [-o | --output <output filename>]\n")
    print("-x | --x86                   Run the x86 toolchain.")
    print("-a | --arm                   Run the arm toolchain.")
    print("-v | --verbose               Show some information about steps performed.")
    print("-g | --gdb                   Run gdb command on executable.")
    print("-b | --break <break point>   Add breakpoint after running gdb. Default is _start.")
    print("-r | --run                   Run program in gdb automatically. Same as run command inside gdb env.")
    print("-q | --qemu                  Run executable in QEMU emulator. This will execute the program.")
    print("-32| --x86-32                Compile for 32bit (x86-32) system (x86 toolchain).")
    print("-p | --port                  Specify a port for communication between QEMU and GDB. Default is 12222 (arm toolchain).")
    print("-o | --output <filename>     Output filename.")

    sys.exit()  # Exit after printing the user guide

# Default arguments
TOOLCHAIN = ""
VERBOSE = False
GDB = False
BREAK = "_start"
RUN = False
QEMU = False
BIT64 = True
PORT = "12222"
OUTPUT_FILE = ""

# Investigating and updating flags
for i in range(len(sys.argv)):
    arg = sys.argv[i]
    if arg == "-x" or arg == "--x86":
            if TOOLCHAIN == "": #Error check to ensure only one toolchain is selected
                TOOLCHAIN = "x86"
            else:
                print("Cannot use both toolchains!")
                sys.exit()
    elif arg == "-a" or arg == "--arm":
            if TOOLCHAIN == "": #Error check to ensure only one toolchain is selected
                TOOLCHAIN = "arm"
            else:
                print("Cannot use both toolchains!")
                sys.exit()
    elif arg == "-v" or arg == "--verbose":
        VERBOSE = True
    elif arg == "-g" or arg == "--gdb":
        GDB = True
    elif arg == "-b" or arg == "--break":
        BREAK = sys.argv[i+1]
    elif arg == "-r" or arg == "--run":
        RUN = True
    elif arg == "-q" or arg == "--qemu":
        QEMU = True
    elif arg == "-32" or arg == "--x86-32":
        BIT64 = False
    elif arg == "-p" or arg == "--port":
        if sys.argv[i+1].isdigit(): # Making sure port number is a number
            PORT = sys.argv[i+1]
        else:
            print("Invalid port number!")
            sys.exit()
    elif arg ==  "-o" or arg == "--output":
        OUTPUT_FILE = sys.argc[i+1]
    else: # Case for unrecognized flag
        if re.search("-.+", sys.argv[i]) or re.search("--.+", sys.argv[i]):
            print(f"Unknown option {sys.argv[i]}")
            sys.exit()

# Ensuring a toolchain has been selected
if TOOLCHAIN == "":
    print("No toolchain selected!")
    sys.exit()

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
    print(f"  TOOLCHAIN = {TOOLCHAIN}")
    print(f"  GDB = {GDB}")
    print(f"  RUN = {RUN}")
    print(f"  BREAK = {BREAK}")
    print(f"  QEMU = {QEMU}")
    print(f"  Input File = {sys.argv[1]}")
    print(f"  Output File = {OUTPUT_FILE}")
    print(f"  Verbose = {VERBOSE}")
    if TOOLCHAIN == "x86":
        print(f"  64 bit mode = {BIT64}\n")
    if TOOLCHAIN == "arm":
        print(f"  Port = {PORT}\n")
    print("NASM started...")

# Run the x86 toolchain
if TOOLCHAIN == "x86":
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

# Run the arm toolchain
if TOOLCHAIN == "arm":
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