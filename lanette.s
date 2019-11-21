.text
.syntax unified
.thumb
.include "event.inc"

@ Warp into Lanette's House; Set ramscript to initiate custom battle

WarpJP:
  ldr r0, warpDest
  ldr r1, hofWarp
  str r1, [r0]
  ldr r1, WarpIntoMap
  bl _call_via_r1
  bl ScriptSetup
  adr r0, CustomMain
  ldr r1, mainAddr
  adds r4, r1, #1
  ldr r2, size
  swi 11 @ CpuSet
  mov lr, r4
  ldr r1, CB2_LoadMap
  bx r1
.align 2
hofWarp:
  .byte 16, 11, 1, 4
mainAddr: .4byte 0x030078AC
size: .4byte 400 @ number of HWORDS

.align 1
ScriptSetup:
  push {lr}
  ldr r0, lanetteFlag
  ldr r1, FlagClear
  bl _call_via_r1
  adr r0, scriptHeader
  ldr r4, gSaveBlock1Ptr
  ldr r4, [r4]
  ldr r1, saveOffset
  adds r4, r1 @ ramscript
  adds r1, r4, #4 @ ramscript *data*
  movs r2, #7 @ size of bootstrap script
  swi 11 @ copy bootstrap 0203184E
  adr r0, CopyScript
  adds r1, #128
  ldr r2, scriptSize
  swi 11 @ copy script
  ldr r1, CalculateRamScriptChecksum
  bl _call_via_r1
  str r0, [r4]
  pop {r0}
  bx r0
.align 2
FlagClear: .4byte 0x0809D040+1
lanetteFlag: .4byte 0x366
gSaveBlock1Ptr: .4byte 0x03005aec
saveOffset: .4byte 0x3728
CalculateRamScriptChecksum: .4byte 0x08098A34+1
scriptHeader: .byte 0x33, 0x14, 0x02, 0x01
bootstrap:
  gotonative 0x02028e49
  goto 0x0203d000

.align 2
CopyScript:
  adr r0, lanetteScript
  ldr r1, scriptDest
  ldr r2, scriptSize
  swi 11
  movs r0, #1
  bx lr
.align 2
scriptSize: .4byte 400
scriptDest: .4byte 0x0203d000
lanetteScript:
  lock
  faceplayer
  msgbox 0x0203d01f, MSGBOX_YESNO
  compare 0x800D, 1
  goto_if_eq 0x0203d044
  msgbox 0x0203d03c
  release
  end
text1: .byte 0xB8, 0xb8, 0xc9, 0xdc, 0xac, 0xfb, 0xbe, 0xdd, 0xd8, 0x00, 0xed, 0xe3, 0xe9, 0x00, 0xd9, 0xe2
       .byte 0xde, 0xe3, 0xed, 0x00, 0xe8, 0xdc, 0xd9, 0x00, 0xce, 0xbb, 0xcd, 0xac, 0xff
text2: .byte 0xc9, 0xdc, 0xb8, 0xc9, 0xc5, 0xb8, 0xb8, 0xff
answerYes: @ 0203d044
  msgbox 0x0203d053
  gotonative 0x0203d0b5
  release
  end
text3: .byte 0xce, 0xdc, 0xd5, 0xe2, 0xdf, 0xe7, 0xab, 0xfb, 0xc3, 0x00, 0xeb, 0xe3, 0xe6, 0xdf, 0xd9, 0xd8
       .byte 0x00, 0xdc, 0xd5, 0xe6, 0xd8, 0x00, 0xe3, 0xe2, 0x00, 0xdd, 0xe8, 0xab, 0xfb, 0xbb, 0xe2, 0xd8
       .byte 0x00, 0xc3, 0x00, 0xdc, 0xd5, 0xea, 0xd9, 0x00, 0xe3, 0xe2, 0xd9, 0x00, 0xe0, 0xd5, 0xe7, 0xe8
       .byte 0xfe, 0xe7, 0xe9, 0xe6, 0xe4, 0xe6, 0xdd, 0xe7, 0xd9, 0x00, 0xda, 0xe3, 0xe6, 0x00, 0xed, 0xe3
       .byte 0xe9, 0xab, 0xfc, 0x0b, 0xa7, 0x01, 0xfb, 0xbb, 0x00, 0xd6, 0xd5, 0xe8, 0xe8, 0xe0, 0xd9, 0xab
       .byte 0xfb, 0xcc, 0xc8, 0xc1, 0xae, 0xe1, 0xd5, 0xe2, 0xdd, 0xe4, 0x00, 0xe8, 0xdc, 0xdd, 0xe7, 0xab, 0xff
.align 1
BattlePatch: @ 0203d0b4
  push {lr}
  push {r2, r3, r4}
  ldr r1, BattleSetup_ConfigureTrainerBattle
  adr r0, battleData
  bl _call_r1
  ldr r1, BattleSetup_StartTrainerBattle
  bl _call_r1
  ldr r0, song
  ldr r1, PlayMapChosenOrBattleBGM
  bl _call_r1
  ldr r0, battleTask
  movs r1, #16
  movs r2, #0
_bpscan: @ scan the task list and change transition type
  cmp r1, #0
  beq _bp1
  strh r2, [r0]
  adds r0, #40
  subs r1, #1
  b _bpscan
_bp1:
  ldr r0, gBattleTypeFlags
  ldr r1, [r0]
  movs r2, #1
  lsls r2, #27
  orrs r1, r2
  str r1, [r0] @ OR with SECRET_BASE
  ldr r1, saveBlock
  ldr r1, [r1]
  ldr r0, baseOffset
  adds r1, r0
  adr r0, baseData
  movs r2, #7 @ size of baseData in HW
  swi 11
  adds r1, #0x34 @ party
  adr r0, party
  movs r2, #48 @ size up to levels
  swi 11
  ldr r0, playerParty
  movs r2, #6
  movs r3, #5
_levelscan:
  cmp r2, #0
  beq _levelset
  ldrb r4, [r0]
  cmp r3, r4
  bhi _bp4
  movs r3, r4
_bp4:
  adds r0, #100 @ 100 bytes per pokemon
  subs r2, #1
  b _levelscan
_levelset:
  adds r1, #96
  adds r2, r1, #6
_bp5:
  cmp r1, r2
  beq _bp6
  strb r3, [r1]
  adds r1, #1
  b _bp5
_bp6:
  movs r0, #1
  pop {r2, r3, r4}
  pop {r1}
_call_r1:
  bx r1
.align 2
BattleSetup_ConfigureTrainerBattle: .4byte 0x080B0D1C+1
PlayMapChosenOrBattleBGM: .4byte 0x0806E0F4+1
song: .4byte 508 @ 471
battleTask: .4byte 0x03005B60+10
BattleSetup_StartTrainerBattle: .4byte 0x080B10CC+1
playerParty: .4byte 0x02024190+84 @ level
gBattleTypeFlags: .4byte 0x02022C90
saveBlock: .4byte 0x03005aec
baseOffset: .4byte 0x1A9C
battleData:
  .byte TRAINER_BATTLE_SINGLE_NO_INTRO_TEXT
  .2byte 1024, 1
  .4byte 0
.align 2
baseData: .byte 0x00, 0x10
trainerName: .byte 0xc7, 0xd9, 0xe6, 0xe6, 0xe4, 0xff, 0xff
trainerID: .4byte 2
.align 2
party: .4byte 1, 1, 0, 0, 0, 0
moves: .2byte 161, 246, 126, 352, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6
species: .2byte 176, 334, 0, 0, 0, 0
items: .2byte 174, 179, 0, 0, 0, 0


.align 2
CustomMain: @ 0x030078AC
  ldr r0, gMain
  adds r0, #0x2c
  movs r1, #1
  strb r1, [r0,#0]
  strb r1, [r0,#2]
MainLoop:
  ldr r1, customFlags
  cmp r1, #0
  beq _skipInput
  ldr r1, ReadKeys
  bl _call_via_r1
_skipInput:
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
  bl TaskScan
  ldr r1, MapMusicMain
  bl _call_via_r1
  ldr r1, WaitForVBlank
  bl _call_via_r1
  b MainLoop

.align 1
TaskScan:
  push {lr}
  ldr r0, gTasks
  movs r1, #16
  ldr r2, badTask
  ldr r3, goodTask
_b2:
  cmp r1, #0
  beq _b3
  ldr r4, [r0]
  cmp r2, r4
  beq intercept
  cmp r3, r4
  beq restore
  adds r0, #40 @ each task is 40 bytes
  subs r1, #1
  b _b2
intercept: @ intercept the soft reset
  ldr r1, ResetTasks
  bl _call_via_r1
  ldr r0, warpDest
  ldr r1, lanetteWarp
  str r1, [r0]
  ldr r1, WarpIntoMap
  bl _call_via_r1
  ldr r1, CB2_LoadMap
  bl _call_via_r1
  b _b3
restore: @ restore input
  adr r0, customFlags
  movs r1, #1
  str r1, [r0]
_b3:
  pop {r0}
  bx r0
.align 2
gTasks: .4byte 0x03005B60
badTask: .4byte 0x08175BD4+1
goodTask: .4byte 0x08175A9C+1
ResetTasks: .4byte 0x080A8818+1
lanetteWarp: .byte 20, 2, 1, 4
.align 2
gMain: .4byte 0x03002360
ReadKeys: .4byte 0x080005E4+1
MapMusicMain: .4byte 0x080A26B0+1
WaitForVBlank: .4byte 0x080008AC+1
warpDest: .4byte 0x02031F84
WarpIntoMap: .4byte 0x08084540+1
CB2_LoadMap: .4byte 0x08085934+1
customFlags: .4byte 0
.align 1
_call_via_r1:
  bx r1
