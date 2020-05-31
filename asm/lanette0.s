.text
.syntax unified
.thumb
.include "asm/event.inc"

@ Universal data writer + SR intercepter

ARMBootstrap: @ Jump into THUMB code
  .4byte 0xE28F0001 @ add pc,#1
  .4byte 0xE12FFF10 @ bx r0
WarpJP: @ 02031834
  ldr r0, warpDest
  ldr r1, hofWarp
  str r1, [r0]
  ldr r1, WarpIntoMap
  bl _call_via_r1
  ldr r0, stackRoot
  mov sp, r0 @ reset stack
  adr r0, CustomMain
  ldr r1, mainAddr
  adds r4, r1, #1
  ldr r2, size
  swi 11 @ Copy custom main to IWRAM
  mov lr, r4  @ Arrange CB2_LoadMap to return to CustomMain
  ldr r1, CB2_LoadMap
  bx r1
.align 2
hofWarp: .byte 16, 11, 1, 4
mainAddr: .4byte 0x030078AC
size: .4byte 400 @ number of HWORDS
stackRoot: .4byte 0x03007f00

.align 2
CustomMain: @ 0x030078AC
  ldr r0, keyInput
  ldrh r0, [r0]
  lsrs r1, r0, #8
  cmp r1, #0 @ L&R
  beq _shift
  cmp r1, #1 @ L
  beq _write
  cmp r1, #2 @ R
  beq _run
  b _after
_shift: @ shift and change address (L&R)
  adr r1, wAddr
  ldr r2, wAddr
  lsls r2, #8
  movs r7, #255
  ands r0, r7
  orrs r0, r2
  str r0, [r1]
  b _skipRead
_write: @ write byte and increment (L)
  adr r1, wAddr
  ldr r2, wAddr
  strb r0, [r2]
  adds r2, #1
  str r2, [r1]
  b _skipRead
_run: @ run code at address (R)
  ldr r1, wAddr
  bl _call_via_r1
  b _skipRead
_after:
  ldr r1, ReadKeys
  bl _call_via_r1
_skipRead:
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
  b CustomMain
.align 2
keyInput: .4byte 0x04000130
wAddr: .4byte 0x0203d000
gMain: .4byte 0x03002360
ReadKeys: .4byte 0x080005E4+1
MapMusicMain: .4byte 0x080A26B0+1
WaitForVBlank: .4byte 0x080008AC+1

.align 1
TaskScan: @ Scan Task list for soft-reset
  push {lr}
  ldr r0, gTasks
  movs r1, #16
  ldr r2, badTask
_b2:
  cmp r1, #0
  beq _b3
  ldr r4, [r0]
  cmp r2, r4
  beq intercept
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
_b3:
  pop {r0}
  bx r0
_call_via_r1:
  bx r1
.align 2
gTasks: .4byte 0x03005B60
badTask: .4byte 0x08175BD4+1
ResetTasks: .4byte 0x080A8818+1
lanetteWarp: .byte 20, 2, 1, 4
warpDest: .4byte 0x02031F84
WarpIntoMap: .4byte 0x08084540+1
CB2_LoadMap: .4byte 0x08085934+1
