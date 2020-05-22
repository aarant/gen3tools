## Addresses
| Symbol | Address |
| ------ | ------- |
| basePtr | 02101D2C |

## Info
- Party PID: pointer + 0xD094 + 0xEC*index
- Tentacruel blockAOff +8 = 0x48
- 0201D5D4 is a decryption routine
- 0207823C computes checksum
- 02074470 takes pokemon in r0, something in r1 & r2
- ignore 0201D5EA, 02074812?, 02074AE6?, 02078248?

- tst [0227e398]?

- sub_02074470
  - r0: pokemon, r1: ?, r2: ?
  - r1 seems to be data type, 5 0x26 grabs species value
  - cry species, item, level:33, ?:0, ?:1, ?:1, type:B, ?:3, OTID:49f67d38, to next level?:287b5, ?:0, ?:94, ?:94, ?:4f, ?:47, ?:51, ?:83, ?:7b, ?:1d, ?:39
  - cry, ., name, ?, ?, ?, species type lookup:02074ae6, ?:02078248, encrypt, decrypt, ?:4812, ?:47d8, ?:8248, encrypt, decrypt, species:47da
  ```
  if pokemon->unused == 0:
    02078234(mon+0x88, 0x64, mon->pid)  # decrypts a block, calls into 0201d5d4
    02078234(mon+8, 0x80, mon->checksum)  # decrypts a block
    calc_checksum = 0207823c(mon+8, 0x80)  # calculates checksum
    if mon->checksum != calc_checksum:
      02022974(?)
      mon->unused |= 4
  r4 = 020744e8(mon, r1, r2)
  if mon->unused == 0:
    0207822C(mon+0x88, 0x64, mon->pid)  # encrypts a block
    0207822C(mon+8, 0x80, mon->checksum)  # encrypts a block
  return r4  # at 020744e6
  ```

- 020747D8 in function 020745d0
  ```
  r4 = species
  if species != 0:
    stuff
  b 02074b26
  return species

  ```
- ~020745b6 in 02074570
  ```
  species = 020745d0()
  return species
  ```
- ~02075f26
  ```
  species = 02074570()
  r4 = species = (species << 16) >> 16
  r0 = mon
  r1 = 0227E378
  r2 = 16
  r0 = 02075d74(?)
  str r0, [sp, 0x18]
  r0 = mon
  r7 = 02075e14(?)
  r0 = mon
  r1 = 0
  r2 = 0
  r6 = 02074570(?)
  r0 = 1EE
  if species != r0:
    r0 = mon
    r1 = 70
    r2 = 0
    r1 = 02074570(?)
  else:
    stuff
  ...@02075f9c
  r1 = species
  02075fb4(?)
    ..r0 = species
    r7 = r3 = 2?
    020761e8(?)
      stuff
    r1 = 1a5
    cmp species, r1
    if species > 0x1A5:
      goto 02076024
    elif species < 0x1A5:
      goto 02075fda
      r2 = 15f
      if species > 0x15F:
        goto 02075ff2
      r1 = 15f
      if species < 0x15F:
        goto 02075fea
        goto 02075ff0 (if not C9)
        goto 020761aa
        r0 = 6
        r1 = 0
        r0 = species * 6
        r2 = r0+r7
        r1 = r1+r2
        r0 += 4
        strh r1, [r5,2] (r5 was 027e3708) @ 020761c4 @ writes halfwords to 027E370A-D (the stack), copied to 022e687e
        r0 += r6
        strh r0, [r5, 4]
      else:
        goto 0207610e
    else:
      goto 020760e4
  ```

- sprite at 022e687e, palette at 022e6880
- sprite read at 02008bb2
  ```
  r0 = 4
  r1 = index
  r2 = 13
  02006ac0(?)
    r0 = 020ffac4
    020069a8(?)
    stuff..
    020c81e4(?) @ 020069ea
    r1 = index*8 + 1c? @ 02006a2c
  ```
- palette read at 02008ff8
