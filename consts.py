OPCODES = [
    "NOP",   # no operation
    "MOV",   # general move
    "SRG",   # set register 0-255 (8 bit)
    "LDR",   # load into reg
    "STR",   # mov current reg to addr
    "SWR",   # swap register value with arg
    "MVR",   # copy (move) register value to arg
    "CMP",   # compare two values
    "CRG",   # compare current register to value
    "PUSH",  # push value to stack
    "POP",   # pop value from stack, move into register arg
    "POPA",  # pop all values from stack
    "POPS",  # pop value from start of stack
    "JMP",   # jump
    "JEQ",   # jump if equal
    "JNE",   # jump not equal
    "JMT",   # jump if more than
    "JME",   # jump if more than or equal to
    "JLT",   # jump if less than
    "JLE",   # jump if less than or equal to
    "INC",   # increment register
    "DEC",   # decrement register
    "ADD",   # add to register
    "SUB",   # sub
    "MUL",   # mul
    "AND",   # and
    "OR",    # or
    "XOR",   # xor
    "NOT",   # not
    "BIT",   # not standard BIT instruction, checks if a bit is one.
    "CALL",  # call subroutine (probably line number?)
    "CLEQ",  # call if values are equal
    "CLNE",  # call if not equal
    "CLMT",  # call if >
    "CLME",  # call if >=
    "CLLT",  # call if <
    "CLLE",  # call if <=
    "CBS",   # call built-in subroutine
    "RET",   # return
    "HALT"   # halt program
]
