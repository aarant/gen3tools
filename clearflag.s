.text
.syntax unified
.thumb
.include "event.inc"

@ Clear Lanette's flag

.align 1
LanetteFlag: @ 03007b00
  ldr r0, flag
  ldr r1, FlagClear
  bx r1
.align 2
FlagClear: .4byte 0x0809D040+1
flag: .4byte 0x366
