.include "event.inc"

.text
.syntax unified
.arm

ScriptHeader: .byte 0x33 0x14 0x02 0x01
Bootstrap:
  gotonative 0x02000000
  goto 0x0203cf64
  end
  end
  .space 128
