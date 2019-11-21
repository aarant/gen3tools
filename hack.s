.text
.syntax unified
.thumb

@ Warp into HOF, set A press, and overwrite AgbMain with custom routine

WarpJP:
  ldr r0, warpDest
  ldr r1, hofWarp
  str r1, [r0]
  ldr r1, WarpIntoMap
  bl _call_via_r1
  adr r0, CustomMain
  ldr r1, mainAddr
  ldr r2, size
  swi 11 @ CpuSet
  subs r1, #199
  mov lr, r1
  ldr r1, CB2_LoadMap
  bx r1
.align 2
hofWarp:
  .byte 16 @ map group
  .byte 11 @ map num
  .byte 1 @ warp
  .byte 4
mainAddr: .4byte 0x030078AC
size: .4byte 100 @ number of HWORDS

.align 2
CustomMain: @ 0x030078AC
  ldr r0, gMain
  adds r0, #0x2c
  movs r1, #1
  strb r1, [r0,#0] @ set pressed to A
  strb r1, [r0,#2] @ set held to A
Loop:
  ldr r7, gMain
  ldr r1, [r7]
  cmp r1, #0
  beq _b0
  bl _call_via_r1 @ call callback1
_b0:
  ldr r1, [r7,#4]
  cmp r1, #0
  beq _b1
  bl _call_via_r1 @ call callback2
_b1:
  ldr r1, MapMusicMain
  bl _call_via_r1
  ldr r1, WaitForVBlank
  bl _call_via_r1
  b Loop
.align 2
gMain: .4byte 0x03002360
MapMusicMain: .4byte 0x080A26B0+1
WaitForVBlank: .4byte 0x080008AC+1
warpDest: .4byte 0x02031F84
WarpIntoMap: .4byte 0x08084540+1
CB2_LoadMap: .4byte 0x08085934+1
.align 1
_call_via_r1:
  bx r1
