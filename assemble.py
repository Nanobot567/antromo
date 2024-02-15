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
    elif origarg.startswith("*"):
        return origarg
    else:
        arg = b"\x00" + int(arg).to_bytes()

    return arg

args = []

functions = {}

def compileASM(data):
    output = b""
    byteCount = 0

    for index, line in enumerate(data.splitlines()):
        line = line.strip()

        opcode = ""
        if line and not line.strip().startswith(";") and not line.isspace():
            try:
                opcode = line.split(" ")[0].upper()
                
                try:
                    args = shlex.split(line, posix=False)[1].split(",")
                except IndexError:
                    args = []

                if opcode == "FUNC":
                    name = line.split(" ")[1]
                    functions[name] = byteCount-1
                else:
                    output += (OPCODES.index(opcode).to_bytes())

                    if opcode in ["MOV", "CMP"]:
                        arg1 = argParse(args[0])
                        arg2 = argParse(args[1])
                        output += arg1
                        output += arg2
                        byteCount += len(arg1)+len(arg2)+1
                    elif opcode in ["SRG","SWR","MVR","CRG","PUSH","POP","JMP","JEQ","JNE","ADD","SUB","MUL","STR","LDR","CALL","CBS"]: # one arg
                        arg1 = argParse(args[0])
                        if opcode == "CALL":
                            arg1 = arg1.strip("*")
                            if arg1 in functions.keys():
                                output += b"\x00"+functions[arg1].to_bytes()
                                byteCount += 3
                            else:
                                output += b"\x00[FUNC "+bytes(arg1, "utf-8")+b"]"
                                byteCount += 3 # fix differences in calling subroutines in different files
                        else:
                            output += arg1
                            byteCount += len(arg1)+1
                    elif opcode in ["NOP", "INC", "DEC", "PRINT", "RET", "HALT"]:
                        # f.write(argParse(args[0]))
                        byteCount += 1

            except ValueError as e:
                print(e)
                print(f"invalid instruction on line {index}: {opcode}")
                return

    for k in functions.keys():
        output = output.replace(b"[FUNC "+bytes(k.strip("*"), "utf-8")+b"]", (functions[k]).to_bytes())

    return output

if __name__ == "__main__":
    f = open(argv[1], "r")

    data = f.read()

    f.close()

    f = open(argv[1].split(".")[0]+".atm", "wb+")

    f.write(compileASM(data))

    f.close()
