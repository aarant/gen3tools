.text
.syntax unified
.thumb

@ Was used for testing

@ Hof:
@   ldr r0, gMain
@   ldr r1, CB1_Overworld
@   str r1, [r0]
@   @ ldr r1, ResetTasks
@   @ bl _call_via_r1
@   ldr r0, gSoftResetDisabled
@   mov r1, #1
@   strb r1, [r0]
@   ldr lr, AgbMain
@   ldr r1, GameClear
@ _call_via_r1:
@   bx r1
@ gMain: .4byte 0x03002360
@ @ ResetTasks: .4byte 0x080A8818+1
@ gSoftResetDisabled: .4byte 0x030027A0
@ AgbMain: .4byte 0x080004B2+1
@ GameClear: .4byte 0x081377A4+1
@ CB1_Overworld: .4byte 0x0808576C+1

@ Credits: @ 020302D0 working
@   ldr r0, gTasks
@   ldr r1, hofDisplay
@   str r1, [r0]
@   ldr r0, scriptPtr
@   mov r1, #0xff
@   strb r1, [r0,#0xc]
@   ldr r0, [r0]
@   mov r1, #6
@   strb r1, [r0]
@   bx lr
@ gTasks: .4byte 0x03005b60
@ hofDisplay: .4byte 0x08173F69
@ scriptPtr: .4byte 0x02038090

@ oldTeleport: @ working
@   mov r0, #13 @ map group
@   mov r1, #8 @ map num
@   ldr r2, LoadMap
@   bl _call_via_r2
@   ldr lr, AgbMain
@   ldr r2, OvoReturn
@ _call_via_r2:
@   bx r2
@ LoadMap: .4byte 0x08084A00+1
@ AgbMain: .4byte 0x080004B2+1
@ OvoReturn: .4byte 0x0803DBB0+1

@ Teleport: @ working
@   ldr r0, warpDest
@   ldr r1, warpData
@   str r1, [r0]
@   ldr r0, WarpIntoMap
@   bl _call_via_r0
@   ldr lr, AgbMain
@   ldr r0, CB2_LoadMap
@ _call_via_r0:
@   bx r0
@ warpDest: .4byte 0x02031F84
@ warpData:
@   .byte 13 @ map group
@   .byte 8 @ map num
@   .byte 1 @ warpId
@   .byte 4
@ WarpIntoMap: .4byte 0x08084540+1
@ CB2_LoadMap: .4byte 0x08085934+1
@ AgbMain: .4byte 0x080004B2+1

@ TeleportUS: @ working
@   ldr r0, warpDest
@   ldr r1, warpData
@   str r1, [r0]
@   ldr r0, WarpIntoMap
@   bl _call_via_r0
@   ldr lr, AgbMain
@   ldr r0, CB2_LoadMap
@ _call_via_r0:
@   bx r0
@ warpDest: .4byte 0x020322e4
@ warpData:
@   .byte 25 @ map group
@   .byte 40 @ map num
@   .byte 1 @ warpId
@   .byte 4
@ WarpIntoMap: .4byte 0x08084bd8+1
@ CB2_LoadMap: .4byte 0x08085fcc+1
@ AgbMain: .4byte 0x080004B2+1

@ Teleport JP
.byte 0
.2byte 0x1D34
.2byte 0xDF05
