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

- arguments in opcodes are separated by commas `,` (if you would like to use the comma character, escape it with `\`.)
- pointers to RAM addresses are signified by the `#` prefix.
- binary values are signified by the `%` prefix.
- char values are surrounded by single quotes `'`
- string values are possible when storing to registers, signified by double quotes `"`
- if you would like to refer to the location of a subroutine, prefix it with an asterisk `*`
- `;` is the comment signifier

files can be included into the current one with `include`:

```
include "otherfile.atms" ; contains 'ldr "hello!"'

cbs 'P'
```

constants can be defined with `define` and called with `@`:

```
define TEXT "hello\, world!!"

ldr @TEXT
cbs 'P'
```

labels can be defined with the `lbl` keyword.

```
srg 0
ldr "Hello world"
call *print

lbl print
    cbs 'P'
    ret
```

### keyboard input

address `0x25` contains the keycode for the key currently pressed. all keycodes are normal, except for the arrow keys:

- left: `1`
- up: `2`
- right: `3`
- down: `4`
- enter: `5`
- backspace: `6`
- space: `32`

### compiling and running

you can either run `python3 assemble.py (PROGRAM_NAME)` to get a `.atm` file, or you can run the `.atms` directly with `antromo.py`.
