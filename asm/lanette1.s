.text
.syntax unified
.thumb
.include "asm/event.inc"

@ Task scanner/interceptor, to preempt THE END soft reset

.align 2
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
