#! /bin/python3

# antromo assembler

from sys import argv
import shlex

from consts import OPCODES

# # is pointer
# % is binary
# ' ' is char
# " " is string
# none is just number


def argParse(arg=""):
    arg = arg.strip()
    origarg = arg

    # the starting byte is the type identifier. instead of making every op a seperate instruction, why not just one extra type byte :)
    # add hexadecimal number mode

    # figure out a way to write to large RAM addresses

    if origarg.startswith("#"):
        arg = b"\x01" + int(arg.strip("#")).to_bytes()
    elif origarg.startswith("%"):
        arg = b"\x00" + int(arg.strip("%"), 2).to_bytes() # probably just make \x02 into \x00
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
    else:
        arg = b"\x00" + int(arg).to_bytes()

    return arg

args = []

def compileASM(data):
    output = b""

    for index, line in enumerate(data.splitlines()):
        opcode = ""
        if line and not line.strip().startswith(";") and not line.isspace():
            try:
                opcode = line.split(" ")[0].upper()
                output += (OPCODES.index(opcode).to_bytes())

                try:
                    args = shlex.split(line, posix=False)[1].split(",")
                except IndexError:
                    args = []

                if opcode in ["MOV", "CMP"]:
                    output += (argParse(args[0]))
                    output += (argParse(args[1]))
                elif opcode in ["SRG","SWR","MVR","CRG","PUSH","POP","JMP","JEQ","JNE","ADD","SUB","MUL","STR","LDR","KEY"]: # one arg
                    output += (argParse(args[0]))
                elif opcode in ["NOP", "INC", "DEC", "PRINT", "HALT"]:
                    # f.write(argParse(args[0]))
                    pass

            except ValueError as e:
                print(e)
                print(f"invalid instruction on line {index}: {opcode}")
                return

    return output

if __name__ == "__main__":
    if not len(argv) == 2:
        print("usage: %s [file]" % (argv[0]))
        exit(0)


    f = open(argv[1], "r")

    data = f.read()

    f.close()

    f = open(argv[1].split(".")[0]+".atm", "wb+")

    f.write(compileASM(data))

    f.close()
