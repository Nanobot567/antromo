#! /bin/python3

# antromo assembler

import re
from sys import argv
import shlex
from os import path

from consts import OPCODES

# # is pointer
# % is binary
# ' ' is char
# " " is string
# none is just number

debug = False

def argParse(arg=""):
    arg = arg.strip()
    origarg = arg

    # the starting byte is the type identifier. instead of making every op a seperate instruction, why not just one extra type byte :)
    # add hexadecimal number mode

    # figure out a way to write to large RAM addresses

    # if origarg.startswith("@") or origarg[1] == "@":
    #     origarg = origarg.replace("@".join(origarg.split("@")[1:]), origarg.split("@")[0]+variables[origarg.strip("@")])

    # figure out how to replace any variable with @ before with var value

    if origarg.startswith("#"):
        arg = b"\x01" + int(arg.strip("#")).to_bytes()
    elif origarg.startswith("%"):
        arg = b"\x00" + int(arg.strip("%"), 2).to_bytes()
    elif origarg.startswith("'"):
        arg = arg.strip("'")
        arg = arg.replace("\\n","\n")
        arg = b"\x00" + ord(arg).to_bytes()
    elif origarg.startswith("\""):
        origarg = arg.strip("\"")
        origarg = origarg.replace("\\n","\n")
        arg = b"\x02"

        for i in origarg:
            arg += ord(i).to_bytes()
        
        arg += b"\x00" # null terminator
    elif origarg.startswith("*"):
        return origarg
    elif origarg.startswith("@"):
        return variables[origarg.strip("@")]
    else:
        arg = b"\x00" + int(arg).to_bytes()

    return arg

args = []
variables = {}

functions = {}

def log(data, name="ASM"):
    if debug:
        print(f"[{name}] {data}")

def compileASM(data):
    log("assembling..")

    output = b"ATM"
    byteCount = 3

    for x in re.finditer(r"include\s+(\S+)", data):
        try:
            includefile = open(x.group().split(" ")[1].strip("\""))
        
            data = data.replace(x.group(), includefile.read())

            includefile.close()
        except FileNotFoundError:
            print(f"ERR: include file not found: {x.group()}")
            exit(1)
    

    for index, line in enumerate(data.splitlines()):
        line = line.strip()

        opcode = ""
        if line and not line.strip().startswith(";") and not line.isspace():
            try:
                opcode = line.split(" ")[0].upper()

                log(f"found opcode {opcode} on line {index}")
                
                try:
                    tempargs = []
                    shlexthing = shlex.split(line, posix=False)

                    for i in shlexthing[1:]:
                        tempargs += re.split(r'(?<!\\),', i)
                        
                    args = tempargs

                    for i,v in enumerate(args):
                        args[i] = v.replace("\\,",",")
                    log(f"args: {args}")
                except IndexError:
                    args = []

                if opcode == "LBL":
                    name = line.split(" ")[1]
                    functions[name] = byteCount
                    log(f"found LBL {name} for byte {byteCount-1}")
                elif opcode == "DEFINE":
                    variables[args[0]] = argParse(args[1])
                    log(f"found DEFINE '{args[0]} = {args[1]}'")
                else:
                    output += (OPCODES.index(opcode).to_bytes())

                    if opcode in ["NOP", "POPA", "NOT", "INC", "DEC", "RET", "HALT"]: # no args
                        # f.write(argParse(args[0]))
                        byteCount += 1
                    elif opcode in ["MOV", "CMP"]: # two args
                        arg1 = argParse(args[0])
                        arg2 = argParse(args[1])
                        output += arg1
                        output += arg2
                        byteCount += len(arg1)+len(arg2)+1
                    else: # one arg (since these are more common)
                        arg1 = argParse(args[0])
                        if str(arg1).startswith("*"):
                            arg1 = arg1.strip("*")
                            if arg1 in functions.keys():
                                output += b"\x00"+functions[arg1].to_bytes()
                                byteCount += 3
                                log("found LBL pointer")
                            else:
                                output += b"\x00[FUNC "+bytes(arg1, "utf-8")+b"]"
                                byteCount += 3 # fix differences in calling subroutines in different files
                                log("found LBL pointer, LBL not found")
                        else:
                            output += arg1
                            byteCount += len(arg1)+1

                log(f"moved to byte {byteCount}")


            except ValueError as e:
                print(f"invalid instruction on line {index}: {opcode}")
                return
            except IndexError as e:
                print(f"instruction {opcode} takes more than {len(args)} arguments")
                return

    for k in functions.keys():
        output = output.replace(b"[FUNC "+bytes(k.strip("*"), "utf-8")+b"]", (functions[k]).to_bytes())

    return output

if __name__ == "__main__":
    if len(argv) == 3 and argv[2] == "-v":
        debug = True
        log("verbose mode ON", "ASSEMBLER")
    elif not len(argv) == 2:
        print("usage: %s [file] (-v)" % (argv[0]))
        exit(1)
        
    if not path.exists(argv[1]):
        print("error: no such file or directory: '%s'" % (argv[1]))
        exit(1)

    f = open(argv[1], "r")

    data = f.read()

    f.close()

    f = open(argv[1].split(".")[0]+".atm", "wb+")

    f.write(compileASM(data))

    f.close()
