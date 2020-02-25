.text
.syntax unified
.thumb
.include "event.inc"

@ Custom event graphics test

.align 1
CustomEvent:
  ldr r4, eventTemplate
  ldrb r5, [r4,#9] @ movement type
  lsl r5, r5, #0x10
  lsr r5, r5, #0xe
  ldr r1, sMovementTypeCallbacks
  add r5, r1, r5
  ldr r5, [r5] @ callback
  bl _pseudoMakeObject
_pseudoMakeObject:
  push {r4, r5, r6, lr}
  ldr r0, graphics
  ldr r4, spriteTemplate
  ldr r6, subspriteTables
  ldr r1, MakeObjectTemplateFromEventObjectTemplate
_call_via_r1:
  bx r1
.align 2
spriteTemplate:
spriteFrameImage:
subspriteTables:
eventTemplate:
sMovementTypeCallbacks:
graphics: .4byte 0
MakeObjectTemplateFromEventObjectGraphicsInfo: .4byte 0x0808D66C+1+7*2
