# Emerald (U) TAS Notes
## Symbols
| Symbol | Address |
| ------ | ------- |
| gTrainerId | 02020000 |
| RNG | 03005D80 |
| RNG cycles | 020249c0 |
| gSaveBlock1Ptr | 03005d8c |
| gsaveBlock2Ptr | 03005d90 |
| party | 020244ec |
| gRandomTurnNumber | 02024330 |
| gBattleMons | 02024084 |
| gMoveResultFlags | 0202427c |
| gCritMultiplier | 02024211 |
| gBattleMoveDamage | 020241f0 |
| tileTransitionState | 02037593 |
| enemy party | 02024744 |
| sBattleAnimScriptPtr | 020383f0 |
| gAnimFramesToWait | 020383fc |
| gAnimScriptActive | 020383fd |
| visual task count | 020383fe |
| sound task count | 020383ff |
| gTasks | 03005e00 |
| load animation | 080A3B58 |
| CalculateBoxMonChecksum | 08068c78 |
| GetSpeciesName | 0806b914 |
| CreateBoxMon | 08067bbc |
| CreateMon | 08067b4c |
| gEventObjects | 02037350 |
| InitEventObjectStateFromTemplate | 0808d644
| TrySpawnEventObjects | 0808df80
| ClearEventObject | 0808d3f0 |
| ResetEventObjects | 0808d438 |
| LoadEventObjects | 08076e64
| GetRamScript | 08099188 |
| Box Names | 02031B70 |
| GiveBoxMonInitialMoveset | 08069270
| moveset loop | 080692C2 |
| gWishFutureKnock | 020243d0 |
| gBattleTypeFlags | 02022fec |
| gLastUsedItem | 02024208 |
| CB2_LoadMap2 | 08085fcc |
| GiveBoxMonInitialMoveset | 08069270 |

# Marking ACE
- Markings memcpy'd to 020032C0
- return is 0806901B (BoxMonToMon)
- return to 081C00E7 (CopyMonToSummaryStruct)
- return to 081BFC43 (SummaryScreen_LoadGraphics)
... later
- accessed 0806A952 (GetBoxMonData)
- return to 0806A66F (GetMonData)
- return to 081C49A7 (CreateMonMarkingsSprite)
- StartSpriteAnim(020207C8, u8 markings)
  - sprite->animNum = markings (020207F2)
... LATER
- accessed 080076B6 (BeginAnim)
... later
- accessed 08007796 (ContinueAnim)
... animation delay
- accessed 080077E2 (ContinueAnim)
- anims = u32 at 020207C8 (0859EFA4?)
- foo = u32 at anims+markings*4
- pretype = foo+cmd*4 (cmd is 1?)
- funcindex = 3
- type = ldrsh pretype + 0
- @ 080077F4
- if type < 0: funcindex = type + 3
- call u32 at 082EC6D4+4*funcindex (an animCmd)
- 41: 00000000
- 42: 6821D20C
- 43: 00000C00
- 44: E3500801
- 45: 2F5A082D
- 46: 00000000
- 47: 00000C00

## Mail Glitch?
- gSaveBlock1 + 0x2BE0 + slot*0x24 (0x2BE0 + 0xFF*0x24 = 0x4FBC)
- edits substruct_1[3:]-substruct_2[:10] of box 2 slot 27
- gWishFutureKnock flags: 020243F9
- BATTLE_TYPE_SECRET_BASE 0x8000000

## New Route:
- Mudkip:
- Target EVs: 17 HP 6 AT (HP Up, Kelpsy Berry, Wurmple, Solrock, Poochyena)
- Order: Any Abra Marshtomp
- Rose fight: KO Any, bring Abra to 1, switch to Marshtomp (this updates slot to 3)
- Teleport to Petalburg, apply vitamins/berries
- Name Box 1, scroll back to box 2 in reverse, deposit Marshtomp Box 2 SLot 24
- Corrupt PID & Withdraw Egg
- Hatch. Win.
- alternate routes: Which HP Up, Verdanturf early/late

## Front Sprite ACE Targets
```
Species Address  EVs
085B =  0206FFFF (091 HP 008 AT) X
08B7 =  0206FFFF (183 HP 008 AT) X
0A8C =  0206FFFF (140 HP 010 AT) X
40E9 =  0206FFFF (233 HP 064 AT) Y - Works when hatching or viewed in summary
45BB =  0206FFFF (187 HP 069 AT) X
E692 =  0206FFFF (146 HP 230 AT) X

0525 =  02FE0600 (037 HP 005 AT) X
0599 =  0206FEFE (153 HP 005 AT) X
0611 =  0206FEFE (017 HP 006 AT) Y - (Only when hatching)
0673 =  82847F80 (115 HP 006 AT) X
0737 =  82847F80 (055 HP 007 AT) X
0799 =  0206FEFE (153 HP 007 AT) X
09F7 =  02020000 (247 HP 009 AT) X
0A04 =  02FE0600 (004 HP 010 AT) X
0A3B =  0206FEFE (059 HP 010 AT) X
0A3E =  02020000 (062 HP 010 AT) X
0A5E =  0206FEFE (094 HP 010 AT) X
0A7B =  02FE0600 (123 HP 010 AT) X
0AAA =  02FE0600 (170 HP 010 AT) X
0B15 =  02020000 (021 HP 011 AT) X
0B50 =  82847F80 (080 HP 011 AT) X
0B59 =  0206FEFE (089 HP 011 AT) X
0B99 =  02FE0600 (153 HP 011 AT) X
```

## Front Sprite ACE Targets (FR)
```
Species Addr    EVS             (H)atch/(S)ummary
0611 = 0206fefe (017 HP 006 AT) H
0a3b = 0206fefe (059 HP 010 AT) x
411d = 0206fefe (029 HP 065 AT) x
085b = 0206ffff (091 HP 008 AT) x
0b59 = 0206fefe (089 HP 011 AT) H
0a5e = 0206fefe (094 HP 010 AT)
4139 = 0206fefe (057 HP 065 AT)
0a8c = 0206ffff (140 HP 010 AT)
0599 = 0206fefe (153 HP 005 AT)
0799 = 0206fefe (153 HP 007 AT)
4166 = 0206fefe (102 HP 065 AT)
4176 = 0206fefe (118 HP 065 AT)
08b7 = 0206ffff (183 HP 008 AT)
e905 = 0206fefe (005 HP 233 AT)
41bf = 0206fefe (191 HP 065 AT)
ea22 = 0206fefe (034 HP 234 AT)
ea25 = 0206fefe (037 HP 234 AT)
45cf = 0206ffff (207 HP 069 AT)
fe20 = 0206fefe (032 HP 254 AT)
40e2 = 0206fefe (226 HP 064 AT)
40e6 = 0206fefe (230 HP 064 AT)
e642 = 0206fefe (066 HP 230 AT)
40ed = 0206ffff (237 HP 064 AT)
ff49 = 0206fefe (073 HP 255 AT)
fd5c = 0206fefe (092 HP 253 AT)
ff5e = 0206ffff (094 HP 255 AT)
fd7a = 0206fefe (122 HP 253 AT)
e6a6 = 0206ffff (166 HP 230 AT)
f5a2 = 0206fefe (162 HP 245 AT)
```
## Sprite ACE
- Acquire DOTS, or a similar corruption target, with (233 HP, 64 AT) EVs
- Place in Box 2 Slot 24
- Corruption target address is 0202A8D0
- Acquire species 0x40E9 via single or double corruption
- Name Box 1 (x♂xC). This ensures that when hatching, the animation won't crash
- If single corruption + hatching, nickname it the THUMB bootstrap and place it in Box 12 Slot 4
- If double corruption, name a pokemon the THUMB bootstrap and place in Box 12 Slot 3
- Place ARM code starting in Box 12 Slot 13 and every 10 slots after
- THUMB target address is 0206FFFF (Box 12 Slot 3 nickname)

# Testing Abra corruption frames
```
RNG       Cycle   PID      Works?
37D87E94  692     6C905417 N
D14C4059  855     A09DD804 Y
2D610993  929     10C751B5 N
7719D16C  1292    FF6EE2B3 N
9C9BC078  1400    EC5E800E N
F03F0A98  1432    4B703247 N
3EBA17DE  1654    915D1DC7 Y
```

# 855 Abra Corruption results
- 18/32 corrupt nothing
- 1/32 corrupts PID (good Egg)
- 1/32 corrupts TID (other, bad Egg) if and only if SID is bad
- 6/32 corrupt data that can never cause a Bad Egg
- 6/32 corrupt substructure data that can cause a Bad Egg

Bad Eggs can only occur if !(SID & 0x4000), i.e if your SID's uppermost nibble is 0, 1, 2, 3, 8, 9, A, B (1/2 chance)
```
0202Axxx
Address Corrupted
89C     substruct_1[11]
8A0     substruct_1[7] (exp)
8A4     substrict_1[3]
8A8     substruct_0[11] (sheen)
8AC     substruct_0[7] (beauty)
8B0     substruct_0[3] (speed EV)
8B4     Trash bytes
8B8     Markings
8BC     4th character of OT
8C0     unused egg flags
8C4     8th character of nickname
8C8     4th character of nickname
8CC     TID/SID (other egg in Luxury/Premier Ball)
8D0     PID (what we want)
8D4     Nothing
8D8     Nothing
8DC     Nothing
8E0     Nothing
8E4     Nothing
8E8     Nothing
8EC     Nothing
8F0     Nothing
8F4     Nothing
8F8     Nothing
8FC     Nothing
900     Nothing
904     Nothing
908     Nothing
90C     Nothing
910     Nothing
914     Nothing
918     Nothing
```

## Front Sprite ACE
r0: 02020784   r1: addr   r2: 00000010   r3: 00000000
r4: 02020784   r5: 020207C2   r6: 00000005   r7: 00000001
r8: 00000000   r9: 00000000  r10: 00000000  r11: 000000
r12: 00000040  r13: 03007EDC  r14: 080069E7  r15: 02070004
cpsr: [-------]
- Preserve r2-r7
- call 08175620
- gSaveBlock1Ptr: 03005d8c
- ARM BX lr at 08000398
- SetBoxMonData: 0806ad9c+1
- DecryptBoxMon: 0806A24C+1
- GameClear: 08137734+1
- OT branch: (EA0000AE) (-  v) (+10 pokemon) or (I  v) (+10 pokemon?)
- Nickname branch: (ea0000b1) ("  v) (+9 pokemon)
### Set pokemon name (WIP)
- target 0206FF4C (Box 11 Slot 30 nickname)
- target 0206FF9C (Box 12 Slot 30 nickname)
- pc is  02071BC4
- diff is 1C28
- diff 1C78
```
box_01: (x♂zN 6FF)
PUSH r2-r3,r5-r7,lr       B5EC @ preserve necessary registers
LDMIA r0!,r1-r3,r5-r7     C8EE @ do not touch r4!
ADD r7,pc,nn              A700 @ (B2 is +9 pokemon ahead)
STMIA r0!,r6,r7           C0C0 @ store new jump address
box_02: (X XxC?” )
                    D200D2FF
POP r2-r3,r5-r7,pc      BDEC
                        B2AC
box_03: (?”FREn  )
                    B2ACFF00
ADC r12,pc,C000     E2BFCCC0 @ r12=pc+C0
box_04: (EhRRn   )
                    BFFF0000
SUBC r12,DC00       E2CCCCDC @ r12=pc-1C01
                    FF000000
box_05: (FG?n5…Rn)
ADC r12,0x30        E2ACC1C0 @ r12=pc-1BD1
SUBC r11,r12,A6     E2CCB0A6 @ r11=target
box_06: ()
                    B2AC00FF
MOV r12,CF          E3B0C0CF @ r12=000000CF
box_07: (?HTF?n  )
                    B2ACFF00
ADC r12,EA          E2ACC4EA @ r12=EA0000CF
box_08: (UFFRn   )
                    BFFF0000
SBC r12,BF          E2CCC0BF @ r12=EA00000F
                    FF000000
box_09: ( F!q  To)
LDRB r0,[r11]       E5DB0000 @ r0=old nickname
BICS r0,0           E3D00000
box_10: ( ?H F…o )
                    B2AC00FF
STRNE r12,[r11]     C5ABC000 @ store nickname
box_11: (?”      )
                    B2ACFF00
SBCNE r11,AD        C2CBB1AD
box_12: (E       )
                    BFFF0000
ADCNE r11,C         C2ABB2C0
                    FF000000
box_13: (  ?”    )
                    B2AC0000
                    00000000

SBCNE r11,50                    C2CBB1C8
STR r12,[r11]       E5ABC000 @ store nickname
BIC r0,lr           E3CE0000
```
### 0x40E9 Map Warp
- Uses THUMB->ARM bootstrap in Box 1-2
- Requires BX r0 in Box 14
```
box_01: (x♂zN 6FF)
PUSH r2-r3,r5-r7,lr       B5EC @ preserve necessary registers
LDMIA r0!,r1-r3,r5-r7     C8EE @ do not touch r4!
ADD r7,pc,nn              A700
STMIA r0!,r6,r7           C0C0 @ store new jump address
box_02: (X XxC?” )
                    D200D2FF
POP r2-r3,r5-r7,pc      BDEC
                        B2AC
box_03: (?”…P-n  )
                    B2ACFF00
ADC r12,lr,B0000    E2AECAB0 @ r12=080B69E7
box_04: (EFQRn   )
                    BFFF0000
SUBC r12,C0000      E2CCCBC0 @ r12=080869E6
                    FF000000
box_05: (…TRnt ?n)
SUBC r12,B00        E2CCCEB0 @ r12=08085EE5
ADC r0,r12,E8       E2AC00E8 @ r0=CB2_LoadMap2
box_06: ( ?”VTTn )
                    B2AC00FF
SUBC r12,lr,D00     E2CECED0 @ r12=08005CE6
box_07: (?”FM?n  )
                    B2ACFF00
ADC r12,3000000     E2ACC7C0 @ r12=0B005CE6
box_08: (ENJRo   )
                    BFFF0000
BIC r12,C8000000    E3CCC4C8 @ r12=03005CE6
                    FF000000
box_09: (5…Bq    )
LDR r11,[r12+A6]    E5BCB0A6 @ r12=saveBlock1
                    00000000
box_10: ( ?”     )
                    B2AC00FF
                    00000000
```
### Change to 0x40E9 (must have BX r0 in Box 14) (experimental)
- party: 020244ec
- TID at 020244F0
- Add to checksum: 0x40E9 - 0x0611 = 0x3AD8
- White out instead of GameClear
- 080069E7 GameClear
- 0813787D SetCB2WhiteOut
```
box_01: (/BGnuTQo)
SUBC r11,r1,BA01    E2C1BCBA @ r11=020644FD
BIC r12,r11,E90     E3CBCEE9 @ r12=0206406D
box_02: ( ?”  Ro )
                    B2AC00FF
BIC r0,r12          E3CC0000 @ r0=0206406D
box_03: (?”AFgm  )
                    B2ACFF00
LDRH r12,[r11+B]    E1DBC0BB @ r12=checksum
box_04: (EdF?n   )
                    BFFF0000
ADC r12,D8          E2ACC0D8
                    FF000000
box_05: (tS?nAFwm)
ADC r12,3A00        E2ACCDE8 @ r12=checksum+0x40E9-0x0611
STRH r12,[r11+B]    E1EBC0BB @ store checksum, r11=02064508
box_06: ( ?”♀Gkm )
                    B2AC00FF
LDRH r12,[pc+0x16]  E1DFC1B6
box_07: (?”IFRo  )
                    B2ACFF00
BIC r12,C3          E3CCC0C3 @ r12=E02CC000 EOR r12,r12,r0
box_08: (E♀FUm   )
                    BFFF0000
STRH r12,[pc+6]     E1CFC0B6
                    FF000000
box_09: (BJgm Fxl) @ lowercase L
LDRH r12,[r11+0x4C] E1DBC4BC @ r12=TID
EOR r12,r12,r0      E0ECC000
box_10: ( ?”’FQm )
                    B2AC00FF
STRH r12,[r11+5]    E1CBC0B4 @ store species
box_11: (?”hT-n  )
                    B2ACFF00
ADC r12,lr,DC0      E2AECEDC @ r12=080077A7
box_12: (EYN?n   )
                    BFFF0000
ADC r12,D30000      E2ACC8D3 @ r12=8D377A7
                    FF000000
box_13: (FNRob ?n)
BIC r12,C00000      E3CCC8C0 @ r12=81377A7
ADC r0,r12,D6       E2AC00D6 @ r0=SetCB2WhiteOut
```
### Lilycove Map Warp (Puts BX r0 in box 14)
- Change map location
- Call CB2_LoadMap2: 08085fcc+1
```
box_01: (mFloyLRo) @ lowercase L
MVN r12,0xe1        E3E0C0E1 @ r12=ffffff1e
BIC r12,0xed>>12    E3CCC6ED @ r12=f12fff1e
box_02: ( ?”m”Ro )
                    B2AC00FF
BIC r11,r12,0xe1>>4 E3CCB2E1 @ r11=BX r0
box_03: (?”…P-n  )
                    B2ACFF00
ADC r12,lr,B0000    E2AECAB0 @ r12=080B69E7
box_04: (EFQRn   )
                    BFFF0000
SUBC r12,C0000      E2CCCBC0 @ r12=080869E6
                    FF000000
box_05: (…TRnt ?n)
SUBC r12,B00        E2CCCEB0 @ r12=08085EE5
ADC r0,r12,E8       E2AC00E8 @ r0=CB2_LoadMap2
box_06: ( ?”     )
                    B2AC00FF
                    00000000
box_07: (?”      )
                    B2ACFF00
                    00000000
box_08: (EFGEn   )
                    BFFF0000
ADC r12,pc,0x30     E2BFC1C0 @ r12=$+38
                    FF000000 +4
box_09: ( …?qVTTn)
STR r11,[r12]       E5ACB000 +8 @ store BX r0
SUBC r12,lr,D00     E2CECED0 +C @r12=08005CE6
box_10: ( ?”FMBn )
                    B2AC00FF +10
ADC r12,3000000     E2BCC7C0 +14 @ r12=0B005CE6
box_11: (?”NJRo  )
                    B2ACFF00 +18
BIC r12,C8000000    E3CCC4C8 +1C @ r12=03005CE6
box_12: (E5…Bq   )
                    BFFF0000 +20
LDR r11,[r12+A6]    E5BCB0A6 +24 @ r12=saveBlock1
                    FF000000 +28
box_13: (VH…o’FQm)
MOV r12,D           E3B0C2D0 +2C @ map group 13:0
STRH r12,[r11+4]    E1CBC0B4 +30
box_14: ( ?”)          
                    B2AC00FF +34
                    yyyyyyyy +38
```
### 0x40E9 Standalone Map Warp
- Change map location
- Call CB2_LoadMap2: 08085fcc+1
- compare at 080692C2 (r0 > r1 to break)
- compare at 080692F8 (r0 == 0xffff to break)
```
box_01: ()
ADD r1,pc,0             A100 @ set jump target
PUSH r1-r4,r6-r7,lr     B5DE @ set up stack
PUSH r5-r7,lr           B5E0
                        0000
box_02: ()
                    D200D2FF
MVN r12,0xe1        C3E0C2E1 @ r12=ffffff1e
box_03: ()
BL                      FFDC @ BX to box_02 in ARM mode
                        D200
BIC r12,0xed>>12    C3CCC6ED @ r12=f12fff1e
box_04: ()
POP r2-r4,r6-r7,pc      BDDC @ restore registers
                        BFFF
BIC r11,r12,0xe1>>4 E3CCB0E1 @ r11=BX r0
                    FF000000
box_05: ()
ADC r12,r7,B0000    E2A7CAB0 @ r12=080B69E7
SUBC r12,C0000      E2CCCBC0 @ r12=080869E6
box_06: ()
                    B2AC00FF
SUBC r12,B00        E2CCCEB0 @ r12=08085EE5
box_07: ()
                    B2ACFF00
ADC r0,r12,E8       E2AC00E8 @ r0=CB2_LoadMap2
box_08: ()
                    BFFF0000
ADC r12,pc,0x34     E2BFC1B0 @ r12=$+3C
                    FF000000 +4
box_09: ()
STR r11,[r12]       E5ACB000 +8 @ store BX r0
SUBC r12,r7,D00     E2C7CED0 +C @ r12=08005CE6
box_10: ()
                    B2AC00FF +10
ADC r12,3000000     E2BCC7C0 +14 @ r12=0B005CE6
box_11: ()
                    B2ACFF00 +18
BIC r12,C8000000    E3CCC4C8 +1C @ r12=03005CE6
box_12: ()
                    BFFF0000 +20
LDR r11,[r12+A6]    E5BCB0A6 +24 @ r12=saveBlock1
                    FF000000 +28
box_13: ()
MOV r12,B10         E3B0CEB1 +30 @ map group 16:11
STRH r12,[r11+4]    E1CBC0B4 +34
box_14: ()
                    yyyyyyFF +38
                    yyyyyyyy +3C @ overwritten with BX r0, return to box_03 in THUMB mode
```
### Inside of Truck
- Group:ID 25:40 or 0x2819
```
box_11: (?”2S…o  ) @ capital S
                    B2ACFF00 +28
MOV r12,28C0        E3B0CDA3 +2C
box_12: (E5FRn   )
                    BFFF0000 +30
SUBC r12,A6         E2CCC0A6 +34 @ r12=map 26:58
                    FF000000 +38
box_13: (’FQm)
STRH r12,[r11+4]    E1CBC0B4 +3C
```
### Southern Island
- Group:ID 26:09 or 0x091A
- TODO: Set the flag
```
box_11: (?”0T…o  ) @ Zero
                    B2ACFF00
MOV r12,A10         E3B0CEA1 +2C    
box_12: (E0H?n   ) @ Zero
                    BFFF0000 +30
ADC r12,A           E2ACC2A1
                    FF000000
box_13: (’FQm)
STRH r12,[r11+4]    E1CBC0B4 +3C
                    xxxxxxxx +40
```
### Navel Rock
- Group:ID 26:66 or 0x421A
- Lavaridge Town is a good spot
```
box_11: (?”CRlo  ) @ lowercase L
                    B2ACFF00 +28
MVN r12,BD00        E3E0CCBD +2c
box_12: (EqFRo   )
                    BFFF0000 +30
BIC r12,E5          E3CCC0E5 +34 @ r12=map 26:66
                    FF000000 +38
box_13: (’FQm)
STRH r12,[r11+4]    E1CBC0B4 +3C
```
### Birth Island
- Group:ID 26:58 or 0x3A1A
```
box_11: (?”wS…o  ) @ capital S
                    B2ACFF00 +28
MOV r12,3AC0        E3B0CDEB +2C
box_12: (E4FRn   )
                    BFFF0000 +30
SUBC r12,A5         E2CCC0A5 +34 @ r12=map 26:58
                    FF000000 +38
box_13: (’FQm)
STRH r12,[r11+4]    E1CBC0B4 +3C
```
### Faraway Island
- Group:ID 26:56 or 0x381A
```
box_11: (?”oS…o  ) @ capital S
                    B2ACFF00 +28
MOV r12,38C0        E3B0CDE3 +2C
box_12: (E4FRn   )
                    BFFF0000 +30
SUBC r12,A5         E2CCC0A5 +34 @ r12=map 26:56
                    FF000000 +38
box_13: (’FQm)
STRH r12,[r11+4]    E1CBC0B4 +3C
```
### Hall of Fame
```
box_11: (?”“T…o  )
                    B2ACFF00 +28
MOV r12,B10         E3B0CEB1 +2C @ map 16:11
box_12: (E  ?”   )
                    BFFF0000 +30
                    B2AC0000 +34
                    FF000000 +38
box_13: (’FQm)
STRH r12,[r11+4]    E1CBC0B4 +3C
```
### 0x611 Map Warps
```
box_01: (mFloyLRo) @ lowercase L
MVN r12,0xe1        E3E0C0E1 @ r12=ffffff1e
BIC r12,0xed>>12    E3CCC6ED @ r12=f12fff1e
box_02: ( ?”m”Ro )
                    B2AC00FF
BIC r11,r12,0xe1>>4 E3CCB2E1 @ r11=BX r0
box_03: (?”…P-n  )
                    B2ACFF00
ADC r12,lr,B0000    E2AECAB0 @ r12=080B69E7
box_04: (EFQRn   )
                    BFFF0000
SUBC r12,C0000      E2CCCBC0 @ r12=080869E6
                    FF000000
box_05: (…TRnt ?n)
SUBC r12,B00        E2CCCEB0 @ r12=08085EE5
ADC r0,r12,E8       E2AC00E8 @ r0=CB2_LoadMap2
box_06: ( ?”lGEn ) @ lowercase L
                    B2AC00FF
ADC r12,pc,0x38     E2BFC1E0 @ r12=$+40
box_07: (?” …?q  )
                    B2ACFF00
STR r11,[r12]       E5ACB000 +8 @ store BX r0
box_08: (EVTTn   )
                    BFFF0000 +C
SUBC r12,lr,D00     E2CECED0 +10 @r12=08005CE6
                    FF000000 +14
box_09: (FMBnNJRo)
ADC r12,3000000     E2BCC7C0 +18 @ r12=0B005CE6
BIC r12,C8000000    E3CCC4C8 +1C @ r12=03005CE6
box_10: ( ?”5…Bq ) @ 5, not S
                    B2AC00FF +20
LDR r11,[r12+A6]    E5BCB0A6 +24 @ r12=saveBlock1
```
### Thumb -> ARM Bootstrap (nickname)
```
box_12_04: @ (x♂zN”6FFxC)
PUSH r2-r3,r5-r7,lr       B5EC @ preserve necessary registers
LDMIA r0!,r1-r3,r5-r7     C8EE @ do not touch r4!
ADD r7,pc,nn              A7B2 @ (B2 is +9 pokemon ahead)
STMIA r0!,r6,r7           C0C0 @ store new jump address
POP r2-r3,r5-r7,pc        BDEC @ restore registers and jump out
```
### Bootstrap with bad ID
```
box_12_03: @ (  x♂”6G'FC)
NOP                       0000
PUSH r2-r3,r5-r7,lr       B5EC @ preserve necessary registers
ADD r7,pc,nn              A7B2
PUSH r0,r6-r7             B4C1
POP r6-r7,pc              BDC0

box_12_12: @ (  zN”6FFxC)
NOP                       0000
LDMIA r0!,r1-r3,r5-r7     C8EE @ do not touch r4!
ADD r7,pc,nn              A7B2 @ (B2 is +9 pokemon ahead)
STMIA r0!,r6,r7           C0C0 @ store new jump address
POP r2-r3,r5-r7,pc        BDEC @ restore registers and jump out
```

### Nickname GameClear
```
box_12_13: @ (mFloyLRo  )
MVN r12,0xe1        E3E0C0E1 @ r12=ffffff1e
BIC r12,0xed>>12    E3CCC6ED @ r12=f12fff1e
box_12_23: @ (m”RoLT-n  )
BIC r11,r12,0xe1>>4 E3CCB2E1 @ r11=BX r0
ADC r12,lr,C60      E2AECEC6 @ r12=08007647
box_13_03: @ (YN?nFNRo  )
ADC r12,D30000      E2ACC8D3 @ r12=8D37647
BIC r12,C00000      E3CCC8C0 @ r12=8137647
box_13_13: @ (z ?n?E0q  )
ADC r0,r12,EE       E2AC00EE @ r0=GameClear
STR r11,[r1+0xFAC]  E5A1BFAC @ write BX r0 to Box 14 Slot 3 OT
```

### Store BX on OT
```
MVN r12,0xe1        E3E0C0E1 @ r12=ffffff1e
BIC r12,0xed>>12    E3CCC6ED @ r12=f12fff1e
BIC r11,r12,0xe1>>4 E3CCB2E1 @ r11=BX r0
STR r11,[r1+0xBEC]  E5A1BFAC @ write BX r0 to Box 13 Slot 29 OT
B+11                EA0000D9
BIC r0,lr
```

### Box Name GameClear
```
box_01: (mFloyLRo)
MVN r12,0xe1        E3E0C0E1 @ r12=ffffff1e
BIC r12,0xed>>12    E3CCC6ED @ r12=f12fff1e
box_02: ( ?”m”Ro )
                    B2AC00FF
BIC r11,r12,0xe1>>4 E3CCB2E1 @ r11=BX r0
box_03: (?”LT-n  )
                    B2ACFF00
ADC r12,lr,C60      E2AECEC6 @ r12=08007647
box_04: (EYN?n   )
                    BFFF0000
ADC r12,D30000      E2ACC8D3 @ r12=8D37647
                    FF000000
box_05: (FNRoz ?n)
BIC r12,C00000      E3CCC8C0 @ r12=8137647
ADC r0,r12,EE       E2AC00EE @ r0=GameClear
box_06: ( ?”FHEn )
                    B2AC00FF
ADC r12,pc,C        E2BFC2C0 @ r12=$+14
box_07: (?” …?q  )
                    B2ACFF00
STR r11,[r12]       E5ACB000 +8
box_08: (E   )
                    BFFF0000 +C
                    FF000000 +10
                    FF000000 +14 (target)
```

## Ram Script ACE
- magic = 51
- address in r2: 0809919E
- call to checksum: 080991BE
- checksum done: 080991C2

## Pomeg Glitch
- starts at 0202A888, goes down by 100 (0x64)
- first 0x40 corruption at 0202A8D0 (Box 2 Slot 24)

RNG initially lags 273 frames, but this diverges over time.

## Power-on to name select
1. Pressing start before the intro saves ~100 frames.
2. Holding a with mid-speed text is faster than fast speed text.
3. Remember to disable move animations and battle shifting!

## Name select & TID/SID generation
TID & SID are 16 bits, with the TID as the lower 16.
- ID offset in saveBlock2: 0xa
1. `SeedRngAndSetTrainerId` is called when the name is confirmed.
    - This seeds the RNG with `REG_TM1CNT_L`, a very fast (>>60hz) timer.
    - `gTrainerId` is set to the same value.
2. Entering the new game calls `InitPlayerTrainerId`.
2. `InitPlayerTrainerId` sets the ID as `Random()<<16+gTrainerId`.
    - This means that `gTrainerId` becomes TID and the random call becomes SID.
    - This call happens 78 frames after the final input to new game

## Truck to Mudkip generation
- Walking out of Brendan's room instead of inspecting the item saves 132 frames.
- "Bumping" can save a few frames.

## Mudkip generation
- From ID generation to earliest mudkip frame is 6992 cycles/frames
- PID is generated 3c/2f after A press
- Method 1 is used

## Battle Mechanics:
- gRandomTurnNumber sometimes set twice? when?
- ai calls RNG some number of times?
- move effects have scripts
- press at when last move text appears
BattleMon HP: +0x28 (each is 0x58 bytes long)
gMoveResultFlags: MISSED is 1
0. BattleAI_ChooseMoveOrAction 08130ba4
   - Called just before FIGHT is shown
1. accuracycheck 08046660 080469E0 23
  - Called 6? frames from move select
  - 3c/1f before gMoveResultFlags set
  acc = gBattleMons[attacker].statStages[STAT_ACC] (by default, 6)
  buff = acc + 6 - gBattleMons[target].statStages[STAT_EVASION]
  calc = sAccuracyStageRatios[buff].dividend * moveAcc
  calc /= sAccuracyStageRatios[buff].divisor
  Hits if (Random() % 100 + 1) <= calc
2. attackstring
2. critcalc 08046c18 08046D82
   - cannot crit in zigzagoon or wally battles
   Crits if !(Random() % [16, 8, 4, 3, 2][chance])
3. damagecalc 08046d8c 08046E40 +2
   - Sets initial gBattleMoveDamage
4. typecalc
5. adjustnormaldamage 080478f4 08047A90 +5
   - Calls Random() again for focus band
   1. ApplyRandomDmgMultiplier
      gBattleMoveDamage \*= 100 - (Random() % 16)
6. seteffectwithchance what does this do?

## Zigzagoon battle
- Cannot score critical hits
- +1 SP

## Brendan 1
- Need two critical hits
- +1 SP

## Wild encounters
- encounters are checked when tileTransitionState == 2
- Takes the value 1c after the transition frame
- 16 frames in between steps (walking)
1. CheckStandardWildEncounter
   - only called if tile transition is 2
    1. StandardWildEncounter (returns true if encounter started) 080b5288
      1. MetatileBehavior_IsLandWildEncounter (continue if true)
      2. DoGlobalWildEncounterDiceRoll (if metatile behaviors different) (return if False) 080b523c 080B525C
         - Immunity for 3-4? steps after encounter
         - return Random() % 100 < 60
      3. DoWildEncounterRateTest(encounterRate, ignoreAbility) (return if False) 080b5144 080B516E
         - rate \*= 80 / 100 if on bike
         - min(rate, 2880)
         - return Random() % 2880 < rate
      4. DoMassOutbreakEncounterTest
      5. TryGenerateWildMon
          1. ChooseWildMonIndex 1
          2. ChooseWildMonLevel 1, 2 if Hustle
          3. CreateWildMon
            1. PickWildMonNature 1
            2. CreateMonWithNature >2
               1. CreateMon
               2. CreateBoxMon

## Trash bytes
- CreateMon
- CreateBoxMon:
  8 pushes, -0x20 (-64 bytes)

## Youngster Calvin
- +1 AT

## Aqua Grunt
- +1 AT

## Youngster Josh
- +1 DE

## Roxanne
- +3 DE

## Hiker Devan
- +2 DE

## Aqua Grunt
- +1 AT

## Brawly
- +1 HP, +1 AT, +1 SP

## Aqua Grunts
- +2 AT, +1 SP

## Pokefan Isabel
- +2 SP

## Pokefan Kaleb
- +2 SP

## Brendan 3
- +1 SA, +3 SP

## Triathlon Alyssa
- +1 SA

## Psychic Edward
- +1 SA

## Wally
- +1 SA

## Youngster Ben
- +1 HP, +1 SP

## Wattson
- +2 SA, +4 SP

## Winstrates?
- Victor: +2 SP
- Victoria: +1 SA
- Vivi: +3 HP, +1 SA
- Vicky: +1 SP
- Total: +3 HP, +2 SA, +3 SP

## Hiker Lucas
- +1 DE, +1 SA

## Hiker Mike
- +1 AT, +2 DE

## Magma Grunts
- +1 SA, +1 SP

## Tabitha
- +1 AT, +2 SA, +1 SP

## Maxie
- +3 AT, +1 SA, +1 SP

## Flannery
- +1 AT, +2 DE, +3 SA

## Petalburg gym rooms
- Speed: +2 SP, can take confusion or defense
- Accuracy: +1 HP, +1 SP, can take defense or recovery
- Confusion: +1 SA, can take Strength
- Defense: +3 HP, can take Strength or OHKO
- Recovery: +1 HP, can take OHKO
- Strength: +2 AT
- OHKO: +2 SP
- Speed, Defense, Strength: +3 HP, +2 AT, +2 SP
- Speed, Confusion, Strength: +2 AT, +1 SA, +2 SP

## Norman
- +3 HP, +1 SA, +4 SP

## Rose & Deandre
- +1 HP, +1 DE, +2 SA, +2 SP

- Total: (9, 14)
- SCS: (6, 14)
- 3 proteins, 1 HP Up: (16, 44)

HP: Marill +2, Jigglypuff (+2)
AT: Nuzleaf (Route 114) +2, Solrock (Meteor Falls) +2
DE: Silcoon, Cascoon, Skarmory +2
SA: Magneton (New Mauville) +2
SD: Lombre (Route 114) +2
SP: Golbat (Meteor Falls), Electrode (New Mauville) +2, Linoone (118) +2

## Move ACE
- Glitch move `0x1608` reads from 02030400 (Box 12, slot 15)
- Target is read from `082c8d6c+(move*4)` (gBattleAnims_Moves)
- Bootstrap: 1f zz yy xx ww 00 (sound task, 0 arguments)
- Bootstrap must be stored in pokemon EVs
- Can only use r10-r14, along with other restrictions, in nickname opcodes
- Smallest jump on trainer name is +10 pokemon, B+195 (ea0000c3)
- Smallest jump on pokemon name is +9 pokemon, B+177 (ea0000b1)

r0: 0 r1: 080a584b r3: 03005e28 r4: 020383f0

### Credits Warp
- Requires trainer name to be the jump (+9 pokemon)
1. Set task to SetCallback2AfterHallOfFameDisplay
2. Hang animation
3. Return
```
ADC r12,r1,0x3a     E2A1C1E8 # r12=0x80A5885
ADC r12,r12,0xe900  E2ACCCE9 # r12=0x80B4185
STH r12,[r4+0xd]    E1C4C0BC # stall animation
ADC r12,r12,0xc0    E2ACCAC0 # r12=SetCallback2AfterHallOfFameDisplay
BIC r11,r3,0xe8     E3C3B0E8 # r11=gTasks
STR r12,[r11]       E5ABC000 # set task
MVN r12,0xe1        e3e0c0e1 # r12=ffffff1e
BIC r12,0xed        e3ccc6ed # r12=f12fff1e
MOV r10,0xc0>10     E3B0A5C0
BIC r12,r12,r10>1   E1CCC0EA # r12=e12fff1e (BX lr)
MOV r10,c6>4        e3b0a2c6
MOV r10,r10<3       e1b0aeea # r10=99
BIC r11,pc          e3cfb000
STR r12,[r11+r10<3] e7abceea # store bx lr ahead of the PC
```

## Input Buffer
gSoftResetDisabled: 03002700
REG_KEYINPUT: 04000130
gMain: 030022c0
callback1: 030022c0
vBlankCallback: 030022cc
heldKeysRaw: 30022e8
```
bootstrap: @ r0: 0 r1: 080a584b r3: 03005e28 r4: 020383f0 r6: addr
  MOV r12,r1>>1 @ r12=04052c25
  ADC r11,r12,0xB @ r11=04052c30

  ADC r11,0xD500 @ r11=04060130
  BIC r11,0xe0000 @ r11=04000130 (REG_KEYINPUT)

  STR r11,[r5] @ store REG_KEYINPUT
  ADC r12,0xEB000000 @ r12=EF052C25

  BIC r11,pc
  STR r12,[r11+r10<3] @ store SWI #5 ahead of the PC
loop:
  SWI #5        EF050000
  LDR r11,[r5] @ r11=REG_KEYINPUT

  LDB r11,[r11] @ r11=keys
  LDR r12,[r6] @ r12=target

  SBC r12,r12,1 @ decrement
  STB r11,[r12] @ write byte

  STR r12,[r6] @ write new target
  xx

  xx
  xx

  yy
```

## Summary ACE??
1. Get a pokemon with ID 0x097d.
2. SummaryScreen_LoadingCB2
  - Loops Load_Graphics until finished
3. SummaryScreen_LoadGraphics 081bfb10 081BFB1E
  1. CopyMonToSummaryStruct
    - r0: pokemon copied (02024550)
    - r3: nickname
  2. ExtractMonDataToSummaryStruct
    - r0: currentMon (points to pokemon)
    - r6: summary struct 0200330C
    Increments a state to extract all data. Returns True when done.
  3. sub_81C25E8 081c25e8
    1. sub_81C2628 081c2628 (if not egg)
      gStringVar1: 02021CC4
      r0: species r1: mon 020032A8
      081C26EE: e813
      081C273E: storing CHAR_SLASH
      081C2750: last StringCopy call
      081C2760: final call to PrintTextOnWindow
      1. SpeciesToPokedexNum, r0=0x8e13
      2. StringCopy
      3. SummaryScreen_PrintTextOnWindow
        1. AddTextPrinterParameterized4
          1. AddTextPrinter
      4. sub_81C228C
        1. sub_8199C30
      5. PutWindowTilemap
      6. Puts species name into strArray <- stack is corrupted here
      7. SummaryScreen_PrintTextOnWindow
        1. AddTextPrinterParameterized4 08199EEC
          1. Sets currentChar to strArray
          2. AddTextPrinter 08199F64
            1. GenerateFontHalfRowLookupTable 080046E2
            2. RenderFont 0x800473A
              called until it returns 1
              gFonts: 03002F80 (ptr)
              loops font function until it != 2
              1. Indexes gFonts with printerTemplate's fontId
              2. fontxFunc where x can be 1..8
                1. RenderText 0800539C
                  TextPrinter: 0202018C
                  0800587A: character is read
                  08005C14: CopyGlyphToWindow

## Back Sprite ACE
- GetSpeciesBackAnimSet: 0817f474
- LaunchAnimationTaskForBackSprite: 0817f594
- after GetNature: 0817F5D0
- store tAnimId at 0817F5EA
- read tAnimId at 0817F4F4 (Task_HandleMonAnimation)
- backAnimSet = sSpeciesToBackAnimSet[species] - 1 (only if not equal to zero)
- animId = 3 * backAnimSet + sBackAnimNatureModTable[nature]
- tAnimId = data[3] = sBackAnimationIds[animId]
- target = sMonAnimFunctions[tAnimId]

- u8 backAnimSet = 0860A8C8[species] - 1
- u8 animId = 3 * backAnimSet + 0860AD2F[nature]
- u8 tAnimId = 0860ACE4[animId]
- u32 target = 0860aa88[4*tAnimId]

## Signature pokemon
- Roxanne: Probopass
- Brawly: Hariyama
- Wattson: Manectric
- Flannery: Torkoal
- Norman: Slaking
- Winona: Altaria
- Tate&Liza: Lunatone&Solrock
- Juan/Wallace: Politoed/Milotic
- Sidney: Shiftry
- Phoebe: Banette/Dusknoir
- Glacia: Glalie/Froslass
- Drake: Salamence/Flygon
- Steven: Metagross
- Archie: Sharpedo
- Maxie: Camerupt
- Zinnia: Whismur/Salamence
