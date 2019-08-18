# Emerald (J) TAS info
ID: f2c73422
Mudkip PID: 9185C80D
pooch: b19006ec
trainer: そ  v EA00000F B+15
glitch id: 0x3110 targets 02330000 (Box 12 slot 13)

## Addresses
| Symbol | Address |
| ------ | ------- |
| gTrainerId | 02020000 |
| party | 02024190 |
| enemy party | 020243E8 |
| RNG | 03005ae0 |
| RNG cycles | 02024664 |
| gSaveBlock1Ptr | 03005aec |
| gSaveBlock2Ptr | 03005af0 |
| animation loaded at | 080A3420 |
| RunAnimScriptCommand | 080a35ac |
| sBattleAnimScriptPtr | 02038090 |
| gAnimFramesToWait    | 0203809c |
| SetCallback2AfterHallOfFameDisplay | 08173F68 |
| gTasks | 03005b60 |
| gRandomTurnNumber | 02023FD4 |
| gBattleMons | 02023D28 |
| gBattleMoveDamage | 02023E94 |
| tileTransitionState | 02037233  |
| gCritMultiplier | 02023EB5 |
| gMoveResultFlags | 02023F20 |

## Mudkip generation
- ~6018 cycles from ID generation
- Lost about 100 frames
- 3c/2f after A press
- +25 frames
- (0, 0, 0, 0, 0, 1)

## Brendan 1
- +25 frames
- (0, 0, 0, 0, 0, 2)

## Youngster Calvin
- (0, 1, 0, 0, 0, 2)
- +5 frames

## Wally Tutorial
1. PutZigzagoonInPlayerParty (just after exiting gym)
  - Generated via method 1
2. StartWallyTutorialBattle (just after message)
   1. CreateMaleMon (loops otId & personality until it's male)
      1. CreateMon
        fixed personality, generates IV
- +200 frames
- TODO: Save frames by stalling in calvin's battle

## Aqua Grunt
- (0, 2, 0, 0, 0, 2)
- +39 frames

## Youngster Josh
- (0, 2, 1, 0, 0, 2)
- +64 frames

## Roxanne
- (0, 2, 4, 0, 0, 2)
- +14 frames

## Move ACE
1. Glitch move `0x3110` targets 02330000 (Box 12 slot 13).
- Bootstrap: 1f zz yy xx ww ff
2. +1 pokemon jumps (B+15) are possible and minimal.
3. ARM instructions fit 1 instruction per pokemon.
4. Use the high registers to avoid clobbering.

r0: 0 r1: 080a5113 r2: ffffffff r3: 03005b88
r4: 020382bc
r8: 0

## Credits Warp (ARM)
1. set task func to SetCallback2AfterHallOfFameDisplay
2. hang animation
3. return
```
ADD r12,r1,0x56     e281c056 # r1=080a5169
ADD r12,r12,0xee    E28ccCEE # r1=080B3F69
ADD r12,r12,0xc0    E28cc80C # r1=08173f69
STR r12,[r3-0x28]   E503c028 # set task
STR r1,[r4-0x22c]   E504122C # hang animation
STB r2,[r4-0x220]   E5442220 # set sound count to ff
BX r1               e12fff1e
```

## Map group (ARM)
1. set map group
2. end animation
3. return
```
LDR r11,[r3-0x9c]   E513B09C # r11=saveBlock1
MOV r12,16          E3A0C010
STB r12,[r11+4]     E5CBC004 # store map
STB r0,[r4-543]     E544021F # make inactive
STB r2,[r4-541]     E544221d # set sound count to ff
BX lr               e12fff1e
```

## Input bootstrap (ARM)
1. setup key input
2. write lower 8 bits consecutively
3. loop until L&R pressed
```
STREQ r0,[r0]       04000130 # dummy instruction. only needed for REG_KEYINPUT
LDR r5,[r6]         E5965000 # r5=REG_KEYINPUT
SWILS #5            9F050000 # C=0 or Z=1
LDR r0,[r5]         E5950000 # R0=keys
STB r0,[r6+0x280]   E5C60280 # store at next
ADD r6,#1           E2866001
AND r0,#0x3f        E2100C3F # Z=L&R
LDRNE r0,[pc-0x198] 143F0198 # pseudo-BNE
```

## Input bootstrap (THUMB)
