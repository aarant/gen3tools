.text
.syntax unified
.thumb

BattlePrint: @ Print text on main window
  ldr r4, BattlePutTextOnWindow
  adr r0, battleText
  movs r1, 0x80 @ windowId 0
  bx r4
.align 2
rngValue: .4byte 0x11223344
.align 2
PatchRng:
  ldr r0, rngAddr
  adr r1, rngAddr
  subs r1, 16 @ rngValue
  ldr r1, [r1]
  str r1, [r0]
  bx lr
.align 2
rngAddr: .4byte 0x03005ae0
BattlePutTextOnWindow: .4byte 0x0814FA04+1
battleText: .string "TASVideos  merrp \nwants to battle!"
