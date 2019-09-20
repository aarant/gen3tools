.text
.syntax unified
.thumb

WarpJP:
  ldr r0, warpDest
  ldr r1, warpData
  str r1, [r0]
  ldr r0, WarpIntoMap
  bl _call_via_r0
  ldr r0, gSoftResetDisabled
  movs r1, #1
  strb r1, [r0]
  ldr r1, AgbMain
  mov lr, r1
  ldr r0, CB2_LoadMap
_call_via_r0:
  bx r0
.space 2
warpDest: .4byte 0x02031F84
warpData:
  .byte 16 @ map group
  .byte 11 @ map num
  .byte 1 @ warp
  .byte 4
gSoftResetDisabled: .4byte 0x030027A0
WarpIntoMap: .4byte 0x08084540+1
CB2_LoadMap: .4byte 0x08085934+1
AgbMain: .4byte 0x080004B2+1
