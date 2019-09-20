.text
.syntax unified
.thumb

Hof:
  ldr r0, gMain
  movs r1, #0
  str r1, [r0] @ null callback1
  ldr r0, gSoftResetDisabled
  movs r1, #1
  strb r1, [r0] @ disable soft reset
  ldr r0, FreeMonSpritesGfx
  bl call_via_r0 @ free heap data
  ldr r0, AgbMain
  mov lr, r0
  ldr r0, GameClear
call_via_r0:
  bx r0
.align 2
gMain: .4byte 0x03002360
gSoftResetDisabled: .4byte 0x030027A0
FreeMonSpritesGfx: .4byte 0x0805ECB0+1
AgbMain: .4byte 0x080004B2+1
GameClear: .4byte 0x081377A4+1
