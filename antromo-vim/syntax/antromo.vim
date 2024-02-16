if exists("b:current_syntax")
  finish
endif

if !exists('main_syntax')
  let main_syntax = 'antromo'
endif

syntax keyword antromoTodos TODO XXX FIXME NOTE

" Match language specific keywords
syntax keyword antromoKeywords
    \ nop
    \ mov
    \ srg   
    \ ldr
    \ str
    \ swr
    \ mvr
    \ cmp
    \ crg   
    \ push
    \ pop
    \ jmp
    \ jeq
    \ jne
    \ jmt
    \ jme
    \ jlt
    \ jle
    \ inc
    \ dec
    \ add
    \ sub
    \ mul
    \ and
    \ or
    \ xor
    \ not
    \ bit
    \ call
    \ cleq
    \ clne
    \ clmt
    \ clme
    \ cllt
    \ clle
    \ cbs
    \ ret
    \ halt

syn keyword antromoStatement lbl nextgroup=antromoFunction skipwhite
syn match antromoFunction '\%([^[:cntrl:][:space:][:punct:][:digit:]]\|_\)\%([^[:cntrl:][:punct:][:space:]]\|_\)*' display contained
syn match antromoFunctionCall '\*\%([^[:cntrl:][:space:][:punct:][:digit:]]\|_\)\%([^[:cntrl:][:punct:][:space:]]\|_\)*'

syntax match antromoNumber "\v<\d+>"
syntax region antromoString start=/"/ skip=/\\"/ end=/"/ oneline
syntax region antromoCharacter start=/'/ skip=/\\'/ end=/'/ oneline

syntax match antromoComment "\v;.*$"

highlight link antromoTodos Todo
highlight link antromoComment Comment
highlight link antromoMarker Comment

highlight link antromoString String
highlight link antromoNumber Number

highlight link antromoOperator Operator
highlight link antromoKeywords Keyword

highlight link antromoCharacter Character

highlight link antromoFunction Function
highlight link antromoFunctionCall Function

highlight link antromoStatement Statement

let b:current_syntax = "antromo"

if main_syntax ==# 'antromo'
  unlet main_syntax
endif
