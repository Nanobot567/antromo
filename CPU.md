# cpu

the antromo fantasy computer uses a custom CPU architecture. all instructions are compiled into bytecode for `antromo.py`.

### instruction set

ordered by opcode number.

| ASSEMBLER INSTRUCTION | ARGUMENTS | DESCRIPTION                                         |
|:---------------------:|:---------:|:---------------------------------------------------:|
| NOP                   | 0         | no operation                                        |
| MOV                   | 2         | general move                                        |
| SRG                   | 1         | set register 0-255                                  |
| LDR                   | 1         | load value into register                            |
| STR                   | 1         | store register value to address                     |
| SWR                   | 1         | swap current register value with register           |
| MVR                   | 1         | move current register value to register             |
| CMP                   | 2         | set compare values                                  |
| CRG                   | 1         | compare current register with value                 |
| PUSH                  | 1         | push value to stack                                 |
| POP                   | 1         | pop value from stack and move it to register        |
| JMP                   | 1         | general jump                                        |
| JEQ                   | 1         | jump if cmp values are =                            |
| JNE                   | 1         | jump if cmp values are !=                           |
| JMT                   | 1         | jump if cmp value one > cmp value two               |
| JME                   | 1         | jump if cmp value one >= cmp value two              |
| JLT                   | 1         | jump if cmp value one < cmp value two               |
| JLE                   | 1         | jump if cmp value one <= cmp value two              |
| INC                   | 1         | increment current register                          |
| DEC                   | 1         | decrement current register                          |
| ADD                   | 1         | add value to current register                       |
| SUB                   | 1         | subtract value from current register                |
| MUL                   | 1         | multiply value by current register                  |
| AND                   | 1         | AND current register with value                     |
| OR                    | 1         | OR current register with value                      |
| XOR                   | 1         | XOR current register with value                     |
| NOT                   | 1         | NOT current register with value                     |
| BIT                   | 1         | if argument bit in byte is 1, sets cmp value 1 to 1 |
| CALL                  | 1         | call subroutine                                     |
| CLEQ                  | 1         | call if cmp values are =                            |
| CLNE                  | 1         | call if cmp values are !=                           |
| CLMT                  | 1         | call if cmp value one > cmp value two               |
| CLME                  | 1         | call if cmp value one >= cmp value two              |
| CLLT                  | 1         | call if cmp value one < cmp value two               |
| CLLE                  | 1         | call if cmp value one <= cmp value two              |
| CBS                   | 1         | call built-in subroutine                            |
| RET                   | 0         | return from subroutine                              |
| HALT                  | 0         | halt program                                        |
