.text
.syntax unified
.thumb

.align 2
monAddr: .4byte 0x02024190
.align 2
BlankMon:
  ldr r4, ZeroMonData
  adr r0, ZeroMonData
  subs r0, 16 @ monAddr
  ldr r0, [r0]
  bx r4
  bx r4
.align 2
ZeroMonData: .4byte 0x08067670+1
