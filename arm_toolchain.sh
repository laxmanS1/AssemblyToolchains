#! /bin/bash    
# the ! ins called a a she bash, and the "/bin/bash" the path to the bash shell in our system sarting from the root directory

#commented by Austin Payne
#itsc204


if [ $# -lt 1 ]; then		# the start of a conditional if statement that pulls some of the code to form the menu that you see on the command line
        echo "Usage:"  #echo is one of bashes many built in functions that can help to pass agruments to the command line this one passes the string of "usage"
        echo "" # this echo command passes a string of empty space to create a break between the previous line and the next line
        echo "arm_toolchain.sh  [-p | --port <port number, default 12222>] <assembly filename> [-o | --output <output filename>]"	#this echo passes an exmple sting of how the implementation of this command  is supposed to look like
        echo "" # this echo ensures that there is a space between the previous line and the next to make in more user reading friendly
        echo "Raspberry Pi 3B default or use '-rp4' to use Raspberry Pi4" # echo passes the arguments of which rasberry Pi you can use if you need this option 
        echo "" # this is another space between the previous line and the next
        echo "-v    | --verbose                Show some information about steps performed." #presents the user with the option verbose and a ort brief discription of what this option does
        echo "-g    | --gdb                    Run gdb command on executable." #presents the user the option to run Rgb debugger to breakdown the code and veiw the stack, heap, registers, and more
        echo "-b    | --break <break point>    Add breakpoint after running gdb. Default is main." # this option is there to allow the user to create a breakpoint in their code, this option is supposed to be used after the users aready ran gdb
        echo "-r    | --run                    Run program in gdb automatically. Same as run command inside gdb env." # this option is to be executed t the same time as the user running the Gdb option
        echo "-rp4  |                          Using Raspberry 4 (64bit)." # this option is meant if your running a 64 bit raspberry Pi code
        echo "-q    | --qemu                   Run executable in QEMU emulator. This will execute the program." # this optino with execute the program in the command line
        echo "-p    | --port                   Specify a port for communication between QEMU and GDB. Default is 12222." # this option is there if the user need to run the code on a specific port
        echo "-o    | --output <filename>      Output filename." # this option takes in the file name

        exit 1 # this exit means this operation is not permitted
fi	#this is used at the end of if statements in bash

POSITIONAL_ARGS=() # this part of the code is here to set all the othere part into their default part until there is a chage that makes them true 
GDB=False		# gdb is set to false unless the users input that option and makes the GDB part of the code true
OUTPUT_FILE="" # it to start empty unitl the user inputs the file name
VERBOSE=False # set to default to false until the user inputs this option and makes it true 
QEMU=False #set to default to false until the user inputs this option and makes it true 
PORT="12222" # this is the default port that the program will run at unless specified
BREAK="main" # will set a break  automatically unless specified
RUN=False #set to default to false until the user inputs this option and makes it true 
RP3B=True  # default Raspberry Pi 3B, unless you need to used RP4
RP4=False  #set to default to false until the user inputs this option and makes it true 

while [[ $# -gt 0 ]]; do # tis it the start of the while loop that takes in the users input for which option they need
        case $1 in # casing is for if they choose a specific option that option becomes true and the program now neew to run that part of the code, casing is also a a simpler form of if-else statements and keeps the code neater and still readable
                -g|--gdb)
                        GDB=True # this is the bolean logic where if this becomes truethe rest of this part of casing will execute
                        shift # a shift happens when this option becomes true and the program "shifts to that part of the code causing that part to execute, this part will shift to the gd part if the option becomes true
                        ;; # ;; is part of the syntax for casing
                -o|--output)
                        OUTPUT_FILE="$2" # ensures that the user has inputted two arguments when trying to uses this part of the program
                        shift # past argument, shifts past the first arguement of the input that the user put in
                        shift # past value, shifts past the second argument the user puts in
                        ;; # part if the systax of casing
                -v|--verbose) # the program will take either option in order to execute verbose
                        VERBOSE=True # check to see if this option is true in the command line, if it is it executes this part of the code, if not it skips over this part
                        shift # past argument, shift to the verbose part of the code down below
                        ;;
                -q|--qemu)
                        QEMU=True # checks to see if any part of the users input makes this statment true, if so it executes this part of the code
                        shift # past argument, shifts to this part of the program down below
                        ;;
                -r|--run)
                        RUN=True # checks to see if any part of the users input makes this statment true, if so it executes this part of the code
                        shift # past argument, shifts to this part of the program down below
                        ;;
                 -rp4|)
                        RP4=True # checks to see if any part of the users input makes this statment true, if so it executes this part of the code
                        RP3B=False # Raspberry Pi 3B will be false as RP4 is used
                        shift # past argument, shifts to this part of the program down below
                        ;;
                -b|--break)
                        BREAK="$2" # looks for the iputed break point that the program is going to stop the code at
                        shift # past argument
                        shift # past value, shifts to this part of the program down below
                        ;;
                -p|--port)
                        PORT="$2", # looks for the inputted port that the program is going to connectto 
                        shift #shifts to this part of the program down below
                        shift
                        ;;
                -*|--*)
                        echo "Unknown option $1" # this is for if the option that has been entered in is unknwon to the program
                        exit 1 
                        ;;
                *)
                        POSITIONAL_ARGS+=("$1") # save positional arg
                        shift #shifts to this part of the program down below
                        ;;
        esac # part of the syntax for casing
done # part of the syntax for the while loop

set -- "${POSITIONAL_ARGS[@]}" # restore positional parameters

if [[ ! -f $1 ]]; then # if none of the options were chosen then print this message and exit the program immediately
        echo "Specified file does not exist"
        exit 1 # exit 1 means that thsi opertion is not permitted
fi # if syntax to end the if statement

if [ "$OUTPUT_FILE" == "" ]; then # this if statment is for executing the output file part of the code
        OUTPUT_FILE=${1%.*} # this part has the modulus operator and the multiplication operator
fi

if [ "$VERBOSE" == "True" ]; then # verbose will run throught this chech list of code and grab the parts of code mentioned in it and execute those parts of the code, and begins the process of compiling, it will also show if each part of the code is true or false at theis moment
        echo "Arguments being set:"
        echo "  GDB = ${GDB}" # will grab the gdb part of the code and run it
        echo "  RUN = ${RUN}" # will grab the RUN part of the program and execute it
        echo "  BREAK = ${BREAK}" # will reb the break part of the program and create a break in the code
        echo "  QEMU = ${QEMU}" # it will run QEMU and go execute on the command line
        echo "  Input File = $1" # shows if its true or false that there is an unknown file tht has been entered in
        echo "  Output File = $OUTPUT_FILE"
        echo "  Verbose = $VERBOSE"
        echo "  Port = $PORT" # grabs the default port or the ort that has been inputted
        echo ""

        echo "Compiling started..." # this message will show on the command line screen when this option is in progress

fi

if [ "$RP3B" == "True" ]; then # this is the if statement that will execute whe the user waants to switch to RP3B 
# Raspberry Pi 3B
arm-linux-gnueabihf-gcc -ggdb -mfpu=vfp -march=armv6+fp -mabi=aapcs-linux $1 -o $OUTPUT_FILE -static -nostdlib &&

fi

if [ "$RP4" == "True" ]; then
# Raspberry Pi 4
arm-linux-gnueabihf-gcc -ggdb -march=armv8-a+fp+simd -mabi=aapcs-linux $1 -o $OUTPUT_FILE -static -nostdlib &&

fi

if [ "$VERBOSE" == "True" ]; then

        echo "Compiling finished" # this is the message that will printot hte screen when this option is finished 

fi


if [ "$QEMU" == "True" ] && [ "$GDB" == "False" ]; then # this if statement makes it so that you can't run gdb and QEMU at the same time, it will only run QEMU witht he file name 
        # Only run QEMU
        echo "Starting QEMU ..."
        echo ""

        qemu-arm $OUTPUT_FILE && echo "" #runs QEMU with the file name and the echo statement down below

        exit 0 #it will exit successfully

elif [ "$QEMU" == "False" ] && [ "$GDB" == "True" ]; then # this statement will only run GDB and won't alow QEMU to run
        # Run QEMU in remote and GDB with remote target

        echo "Starting QEMU in Remote Mode listening on port $PORT ..."
        qemu-arm -g $PORT $OUTPUT_FILE & # this is for if you want to run all of these options together if, your runing  programthe needs a specifi port  and file name 


        gdb_params=()	# takes in these different parameters for the specific port and break point while running gdb
        gdb_params+=(-ex "target remote 127.0.0.1:${PORT}")
        gdb_params+=(-ex "b ${BREAK}")

        if [ "$RUN" == "True" ]; then # this is for if the user wants to run the program alog with executing GDB

                gdb_params+=(-ex "r")

        fi

        echo "Starting GDB in Remote Mode connecting to QEMU ..."
        sudo gdb-multiarch "${gdb_params[@]}" $OUTPUT_FILE && # this line of code is executed with root because of the word sudo and allows the user to run this tool chain almost nywhere in their directories as long as it is set up right

        exit 0 #it will exit successfully

elif [ "$QEMU" == "False" ] && [ "$GDB" == "False" ]; then # this elif statement if both of these options aren't chosen to make sure that they don't run anway and theat the program is executed normally without them
        # Don't run either and exit normally

        exit 0 #it will exit successfully

else			# these are the echoed messages that will print to the terminal if both QEMU and GDB are executed at the same time, it will also tell the user that the defual option that will run will be QEMU
        echo ""
        echo "****"
        echo "*"
        echo "* You can't use QEMU (-q) and GDB (-g) options at the same time."
        echo "* Defaulting to QEMU only."
        echo "*"
        echo "****"
        echo ""
        echo "Starting QEMU ..."
        echo ""

        qemu-arm $OUTPUT_FILE && echo ""
        exit 0 #it will exit successfully

fi
