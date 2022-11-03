# ARM_toolchain: Documentation

## Overview

Created by Lubos Kuzma,ISS Program, SADT, SAIT 
* First stage of program toolchain will help run script on terminal.
* Secondly , default values is  applied for various arguments such as port , GDB,Verbose,Bits,breakpoint, GDB and others if user do not specify
* Next step is using if statement to loop through all the above defined conditions to check the parameters entered by users.
* restore positional parameters entered by user
* If user entered file dose not exist in current directory then it will  show error messenge and exit 
* In next step,if statement is used to loop through conditions to check each parameters and give the output. If Verbose mode is set for true then it will show the details for all the options.
* Finally, if condition is used for compiling ARM64 assembly/QEMU/run and various other parameters.
* At the end , if user enters both options for GDB and QEMU then it will show the message that QEMU and GDB can not be run together and it will run QEMU.



