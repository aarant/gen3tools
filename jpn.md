# Emerald (J) TAS info
ID: f2c73422
Mudkip PID: 9185C80D
pooch: b19006ec
trainer: も  v EA000023 B+35  # TODO: B+15 is possible
glitch id: 0x3110 targets 02330000 (Box 12 slot 13)

## Addresses
| Symbol | Address |
| ------ | ------- |
| gTrainerId | 02020000 |
| party | 02024190 |
| RNG | 03005ae0 |
| RNG cycles | 02024664 |
| gSaveBlock1Ptr | 03005aec |
| gSaveBlock2Ptr | 03005af0 |
| animation loaded at | 080A3420 |
| RunAnimScriptCommand | 080a35ac |
| sBattleAnimScriptPtr | 02038090 |
| gAnimFramesToWait    | 0203809c |
| SetCallback2AfterHallOfFameDisplay | 08173F68 |
| gTasks | 03005b60

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
