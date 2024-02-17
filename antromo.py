#! /bin/python3

# antromo fantasy computer

from pynput import keyboard
from sys import argv, stdout
from os import path

from consts import OPCODES
from assemble import compileASM

debug = False

class AntromoException(BaseException):
    def __init__(self, err):
        self.err = err

    def __str__(self):
        return self.err


if len(argv) == 3 and argv[2] == "--debug":
    debug = True
elif not len(argv) == 2:
    print("usage: %s [file] (--debug)" % (argv[0]))
    exit(1)

if not path.exists(argv[1]):
    print("error: no such file or directory: '%s'" % (argv[1]))
    exit(1)

f = open(argv[1], "rb")

if argv[1].endswith(".atms"):
    data = f.read()
    data = compileASM(data.decode("utf-8"))
else:
    data = f.read()

if not data.startswith(b"ATM"):
    raise AntromoException("not a valid antromo binary file")

f.close()

cmpVal = 0
cmpVal2 = 0
byteIndex = 3
currentKeyCode = 0

registers = []

for i in range(256):
    registers.append(0x0) # possibly make all registers lists so you can fit multiple bytes in them?

currentRegister = 0

randomAccessMemory = []
stack = []
subroutineStack = []

for i in range(256): # 64 KB?
    randomAccessMemory.append(0x0)


def getArg(): # rename?
    global byteIndex
    byteSkip = 0

    if byteIndex + 2 < len(data):
        toset = 0
        formatByte = data[byteIndex+1]

        if formatByte == 0:
            toset = data[byteIndex+2]
            byteSkip = 2
        elif formatByte == 1:
            try:
                toset = randomAccessMemory[data[byteIndex+2]]
                byteSkip = 2
            except IndexError:
                toset = 0
        elif formatByte == 2: # ?
            string = b""

            curSearchByte = 2
            while data[byteIndex+curSearchByte] != 0:
                string += data[byteIndex+curSearchByte].to_bytes()
                curSearchByte += 1

            byteSkip = curSearchByte

            toset = string

        byteIndex += byteSkip

        # print("new byte", byteIndex)

        return toset
    else:
        return 0x0

def keypress(key):
    global currentKeyCode, randomAccessMemory

    try:
        currentKeyCode = key.vk
    except AttributeError:
        pass

    try:
        randomAccessMemory[25] = currentKeyCode
    except IndexError:
        pass # weird index error for no reason
    
def keyrelease(key):
    global currentKeyCode, randomAccessMemory

    currentKeyCode = 0

    try:
        randomAccessMemory[25] = 0
    except IndexError:
        pass

listener = keyboard.Listener(
    suppress=not debug,
    on_press=keypress,
    on_release=keyrelease)
listener.start()

while byteIndex < len(data):
    byte = data[byteIndex]
    opcode = ""
    try:
        opcode = OPCODES[byte]
    except IndexError:
        pass

    if debug:
        print(byteIndex, opcode)
        input()

    if opcode == "MOV":
        arg1 = getArg()
        arg2 = getArg()
        randomAccessMemory[arg1] = arg2
    elif opcode == "SRG":
        currentRegister = getArg()
    elif opcode == "STR":
        arg = getArg()
        randomAccessMemory[arg] = registers[currentRegister]
    elif opcode == "LDR":
        arg = getArg()
        registers[currentRegister] = arg
    elif opcode == "SWR":
        newReg = getArg()
        registers[currentRegister], registers[newReg] = registers[newReg], registers[currentRegister]
    elif opcode == "MVR":
        registers[getArg()] = registers[currentRegister]
    elif opcode == "CMP":
        cmpVal = getArg()
        cmpVal2 = getArg()
    elif opcode == "CRG":
        cmpVal = registers[currentRegister]
        cmpVal2 = getArg()

    elif opcode == "PUSH":
        stack.append(getArg())
    elif opcode == "POP":
        registers[getArg()] = stack.pop()

    elif opcode == "JMP":
        byteIndex = getArg()-1
    elif opcode == "JEQ":
        if cmpVal == cmpVal2:
            byteIndex = getArg()-1
    elif opcode == "JNE":
        if cmpVal != cmpVal2:
            byteIndex = getArg()-1
    elif opcode == "JMT":
        if cmpVal > cmpVal2:
            byteIndex = getArg()-1
    elif opcode == "JME":
        if cmpVal >= cmpVal2:
            byteIndex = getArg()-1
    elif opcode == "JLT":
        if cmpVal < cmpVal2:
            byteIndex = getArg()-1
    elif opcode == "JLE":
        if cmpVal <= cmpVal2:
            byteIndex = getArg()-1


    elif opcode == "INC":
        newval = registers[currentRegister]
        newval += 1
        registers[currentRegister] = newval
    elif opcode == "DEC":
        newval = registers[currentRegister]
        newval -= 1
        registers[currentRegister] = newval
    elif opcode == "ADD":
        newval = registers[currentRegister]
        newval += getArg()
        registers[currentRegister] = newval
    elif opcode == "SUB":
        newval = registers[currentRegister]
        newval -= getArg()
        registers[currentRegister] = newval
    elif opcode == "MUL":
        newval = registers[currentRegister]
        newval *= getArg()
        registers[currentRegister] = newval

    elif opcode == "AND":
        pass
    elif opcode == "OR":
        pass
    elif opcode == "XOR":
        pass
    elif opcode == "NOT":
        pass
    elif opcode == "CALL":
        arg = getArg()
        subroutineStack.append(byteIndex)
        byteIndex = arg
    elif opcode.startswith("CL"):
        passed = False

        if opcode == "CLEQ":
            if cmpVal == cmpVal2:
                passed = True
        elif opcode == "CLNE":
            if cmpVal != cmpVal2:
                passed = True
        elif opcode == "CLMT":
            if cmpVal > cmpVal2:
                passed = True
        elif opcode == "CLME":
            if cmpVal >= cmpVal2:
                passed = True
        elif opcode == "CLLT":
            if cmpVal < cmpVal2:
                passed = True
        elif opcode == "CLLE":
            if cmpVal <= cmpVal2:
                passed = True

        if passed:
            arg = getArg()
            subroutineStack.append(byteIndex)
            byteIndex = arg-1

    elif opcode == "CBS":
        arg = getArg()

        if arg == 67:
            stdout.write("\033c\033[3J") # clears screen
            stdout.flush()
        elif arg == 80:
            try:
                stdout.write(registers[currentRegister].decode("utf-8"))
            except AttributeError: # register is int?
                stdout.write(chr(registers[currentRegister]))

            stdout.flush()
        elif arg == b"PN": # print numerical value
            try:
                stdout.write(str(registers[currentRegister]))
            except AttributeError: # register is int?
                stdout.write(registers[currentRegister])

            stdout.flush()
        
    elif opcode == "RET":
        try:
            byteIndex = subroutineStack.pop()
        except Exception as e:
            pass
            
    elif opcode == "HALT":
        stdout.flush()
        break

    byteIndex += 1

print()
