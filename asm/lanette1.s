.text
.syntax unified
.thumb
.include "asm/event.inc"

@ Set up and copy script

.align 2
ScriptSetup: @ Set flags and copy script into ram script
  push {lr}
  ldr r0, lanetteFlag
  ldr r1, FlagClear
  bl _call_via_r1 @ clear Lanette's flag so she appears
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
  swi 11 @ place into ram script
  ldr r1, CalculateRamScriptChecksum
  bl _call_via_r1
  str r0, [r4] @ store correct checksum
RestoreMarshtomp:
  ldr r0, marshtompPID
  ldr r1, [r0]
  ldr r4, pidClear
  bics r1, r4
  str r1, [r0] @ un-corrupt PID
  movs r1, r0
  ldr r4, BoxMonToMon @ restore HP, stats, etc
  bl _call_via_r4
  pop {r0}
  bx r0
_call_via_r1:
  bx r1
_call_via_r4:
  bx r4
.align 2
FlagClear: .4byte 0x0809D040+1
lanetteFlag: .4byte 0x366
gSaveBlock1Ptr: .4byte 0x03005aec
saveOffset: .4byte 0x3728
marshtompPID: .4byte 0x02024190+200
pidClear: .4byte 0x40000000
BoxMonToMon: .4byte 0x08068b44+1
CalculateRamScriptChecksum: .4byte 0x08098A34+1
scriptHeader: .byte 0x33, 0x14, 0x02, 0x01
bootstrap:
  gotonative 0x02028e49 @ run CopyScript
  goto 0x0203d000

.align 2
CopyScript:
  adr r0, lanetteScript
  ldr r1, scriptDest
  ldr r2, scriptSize
  swi 11 @ place script in fixed position at 0203d000
  movs r0, #1
  bx lr
.align 2
scriptSize: .4byte 400
scriptDest: .4byte 0x0203d000
lanetteScript:
