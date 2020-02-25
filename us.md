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
| moveset loop | 080692C2

## Front Sprite ACE Targets
```
Species Address  EVs
085B =  0206FFFF (091 HP 008 AT) X
08B7 =  0206FFFF (183 HP 008 AT) X
0A8C =  0206FFFF (140 HP 010 AT) X
40E9 =  0206FFFF (233 HP 064 AT) Y - Box 12 Slot 3 Nickname
45BB =  0206FFFF (187 HP 069 AT) X
E692 =  0206FFFF (146 HP 230 AT) X

0525 =  02FE0600 (037 HP 005 AT) X
0599 =  0206FEFE (153 HP 005 AT) X
0611 =  0206FEFE (017 HP 006 AT) X Y - Box 11 Slot 30 Nickname?
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

### Execution Info
r0: 02020784   r1: addr   r2: 00000010   r3: 00000000
r4: 02020784   r5: 020207C2   r6: 00000005   r7: 00000001
r8: 00000000   r9: 00000000  r10: 00000000  r11: 00000000
r12: 00000040  r13: 03007EDC  r14: 080069E7  r15: 02070004
- Preserve r2-r7
- call 08175620
- gSaveBlock1Ptr: 03005d8c
- ARM BX lr at 08000398
- SetBoxMonData: 0806ad9c+1
- DecryptBoxMon: 0806A24C+1
- GameClear: 08137734+1
- OT branch: (EA0000AE) (-  v) (+10 pokemon) or (I  v) (+10 pokemon?)
- Nickname branch: (ea0000b1) ("  v) (+9 pokemon)
### Bootstrap
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

### Hall of Fame Warp
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

```
box_14_3:
MOV r12,B10         E3B0CEB1
STRH r12,[r11+4]    E1CBC0B4
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
