# programming antromo

there is a python file called `assemble.py` which will compile your antromo assembly into bytecode for the interpreter to understand. the syntax is very similar to programming in assembly with NASM.

here is a simple "hello world" in antromo assembly.

```
; hello world

srg 0  ; sets register to 0
ldr "Hello world!\n"  ; sets register 0 to "Hello world\n"
cbs 'P' ; utility function to print to console
```

### assembler

- arguments in opcodes are separated by commas `,`
- pointers to RAM addresses are signified by the `#` prefix.
- binary values are signified by the `%` prefix.
- char values are surrounded by single quotes `'`
- string values are possible when storing to registers, signified by double quotes `"`
- if you would like to refer to the location of a subroutine, prefix it with an asterisk `*`
- `;` is the comment signifier

you can define labels with the `lbl` keyword.

```
srg 0
ldr "Hello world"
call *print

lbl print
    cbs 'P'
    ret
```

### compiling and running

you can either run `python3 assemble.py (PROGRAM_NAME)` to get a `.atm` file, or you can run the `.atms` directly with `antromo.py`.
