.text
.syntax unified
.thumb
.include "event.inc"

@ Custom map loading routine

.align 1
LoadMap: @ 03007b00
  push {lr}
_setup:
  ldr r0, CB2_LoadMap
  bl _call_via_r0
  ldr r0, CB2_ChangeMap
  bl _call_via_r0
  ldr r0, gLastUsedWarp
  ldr r1, warpData
  str r1, [r0]
_gSkip:
  ldr r0, gState
  movs r1, #1
  strb r1, [r0] @ store gMain state to bypass the second LoadCurrentMapData call
_coords:
  ldr r0, dynamicMap
  ldr r1, [r0,#28]
  ldr r2, gSaveBlock1Ptr
  ldr r2, [r2]
  str r1, [r2] @ store x & y
_copyHeader:
  ldr r1, gMapHeader
  movs r2, #14 @ 28 bytes
  swi 11
  bl _pseudo_load
_music:
  ldr r0, dynamicMap
  ldrh r1, [r0,#16]
  ldr r2, gSaveBlock1Ptr
  ldr r2, [r2]
  strh r1, [r2,#0x2c] @ store music
  pop {r0}
  b _call_via_r0
_pseudo_load:
  push {lr}
  push {r4, r5, r6, r7}
  movs r7, #1
  ldr r0, mli0_load_map
_call_via_r0:
  bx r0
.align 2
gLastUsedWarp: .4byte 0x02031F7C
warpData: .byte 24, 106, 1, 0
CB2_ChangeMap: .4byte 0x08137270+1
dynamicMap: .4byte 0x0203d000
gMapHeader: .4byte 0x02036FB8
CB2_LoadMap: .4byte 0x08085934+1
gState: .4byte 0x03002360+0x438
mli0_load_map: .4byte 0x08084AD0+1
gSaveBlock1Ptr: .4byte 0x03005aec
