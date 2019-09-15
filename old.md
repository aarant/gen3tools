# Emerald (J) TAS info
ID: f2c73422
Mudkip PID: 9185C80D
pooch: b19006ec
trainer: そ  v EA00000F B+15
glitch id: 0x3110 targets 02330000 (Box 12 slot 13-14)

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
| gBattleStruct | 02024140 | 0x6d offset
| gMain | 03002360
| inBattle | 03002799
| CreateBoxMon | 080677A0 |
| CreateMon | 08067730 |
| GetSpeciesName | 0806B3DC |
| SetSaveBlocksPointers | 080765E4 |
| save block offset | 080765F6 |
| GetBoxMonData | 0806A1B4 |
| gPokemonStoragePtr | 03005AF4

## Pomeg Glitch
- Target: 0202A52C (-100 each time)

## Trash bytes
- Set at 0806789A
- target byte: 03007cef
- Can be manipulated by opening and closing the menu (lol)

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
- +5 frames
- (0, 1, 0, 0, 0, 2)

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
- +39 frames
- (0, 2, 0, 0, 0, 2)

## Youngster Josh
- +64 frames
- (0, 2, 1, 0, 0, 2)

## Roxanne
- +14 frames
- (0, 2, 4, 0, 0, 2)

## Nickname Abra
- +5 frames
- 1f 50 00 33 02 ff (Box 12 slot 14/15) (まっ ぉい)

## Hiker Devan
- (0, 2, 6, 0, 0, 2)

## Aqua Grunt
- (0, 3, 6, 0, 0, 2)

## Brawly
- +135
- (1, 4, 6, 0, 0, 3)

## Aqua Grunts
- +7
- (1, 6, 6, 0, 0, 4)

## Pokefan Isabel
- +40
- (1, 6, 6, 0, 0, 6)

## Pokefan Kaleb
- +5
- (1, 6, 6, 0, 0, 8)

## Brendan 3
- +99
- (1, 6, 6, 1, 0, 11)

## Triathlon Alyssa
- (1, 6, 6, 2, 0, 11)

## Psychic Edward
- +2
- (1, 6, 6, 3, 0, 11)

## Wally
- (1, 6, 6, 4, 0, 11)

## Youngster Ben
- +6
- (2, 6, 6, 4, 0, 12)

## Wattson
- +41
- (2, 6, 6, 6, 0, 16)

## Hiker Lucas
- +1 DE, +1 SA
- (2, 6, 7, 7, 0, 16)
- 1st Protein

## 2 Solrocks
- (2, 10, 7, 7, 0, 16)

## Hiker Mike
- +1 AT, +2 DE
- 1st HP Up
- (2, 11, 9, 7, 0, 16)

## Verdanturf
- Pick up 2 Fluffy tails, some Pokeballs and X Special?

## Magma Grunts
- +1 SA, +1 SP
- (2, 11, 9, 8, 0, 17)

## Tabitha
- +1 AT, +2 SA, +1 SP
- (2, 12, 9, 10, 0, 18)

## Maxie
- +3 AT, +1 SA, +1 SP
- (2, 15, 9, 11, 0, 19)

## Flannery
- +1 AT, +2 DE, +3 SA
- (2, 16, 11, 14, 0, 19)
- pick up 2nd protein

## Speed Room
- +2 SP
- (2, 16, 11, 14, 0, 21)

## Confusion Room
- +1 SA
- (2, 16, 11, 15, 0, 21)

## Strength Room
- +2 AT
- (2, 18, 11, 15, 0, 21)

## Norman
- +3 HP, +1 SA, +4 SP
- 3rd protein, 2nd HP Up
- (5, 18, 11, 16, 0, 25)

## Ins 1
- (5, 19, 11, 16, 0, 25)
- E5B65190 (90 51 B6 E5) (ゾア♀q)

## Ins 2
- 9F050000 (00 00 05 9F) (  おポ)

## Ins 3
- E5951000 (00 10 95 E5) ( たドq)

## Ins 4
- E4C61001 (01 10 C6 E4) (あたLp)

## Ins 5
- E2110C03 (03 0C 11 E2) (うしちn)

## Ins 6
- 04000130 (30 01 00 04) (ぃあ え)

## Ins 7
- 143F0148 (48 01 3F 14) (ぶあぜと)

## Teach Surf & Facade

## Elixir & HP Up 2
- Elixir: Route 110
- HP Up: Route 111

## Rose & Deandre
- +1 HP, +1 DE, +2 SA, +2 SP
- (6, 19, 12, 18, 0, 27)
- Abra: 1 HP EVs

## Pomeg Berries
- only need 1
- switch Abra into first

## Marill
- Abra: 3 HP EVs

## Route 105/Protein 3
- Use all vitamins
- Knock out 2 Poochyena & bring Abra to 1 HP
- Switch Marshtomp into first

## Route 102
- Knock out 2 Zigzagoon

## Expected EVs
HP-AT DE-SP SA-SD
3110 1d0c 0012
- (16, 49, 12, 18, 0, 29)

## First Deposit
- Put Marshtomp in Box 2 slot 24
- Deposit conscious Poochyena

## Second deposit
- Enter a battle, then deposit first fainted pokemon

## Glitzer Popping
- Use pomeg berry on Abra
- Corrupt PID
- Corrupt TID

# ACE Prep
- Put Mudkip in party
- Put Mudkip and all Poochyena in Box 12 Slot 14
- Use Elixir on Mudkip
- Enable animations!

## Move ACE
1. Glitch move `0x3110` targets 02330000 (Box 12 slot 13).
- Bootstrap: 1f zz yy xx ww ff
- Bootstrap: 1f 50 00 33 02 ff (Box 12 slot 14/15) (まっ ぉい)
2. +1 pokemon jumps (B+15) are possible and minimal.
3. ARM instructions fit 1 instruction per pokemon.
4. Use the high registers to avoid clobbering. (DO NOT use r0)

r0: 0 r1: 080a5113 r2: ffffffff r3: 03005b88
r4: 020382bc
r8: 0

## Using box names
- stored at offset 0x8344 of PokemonStorage
- contiguous in memory?
- target: 02031808

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

## Input Bootstrap
1. setup key input
2. write lower 8 bits consecutively
3. loop until L&R pressed
```
STREQ r0,[r0]       04000130 # REG_KEYINPUT
LDR r5,[r6]         E5965000 # r5=REG_KEYINPUT
SWILS #5            9F050000 # C=0 or Z=1
LDR r1,[r5]         E5951000 # R1=keys
STB r1,[r6+0x280]   E5C61280 # store at next
ADD r6,#1           E2866001
AND r1,#0x3f        E2110C3F # Z=L&R
LDRNE r0,[pc-0x198] 143F0198 # pseudo-BNE
```

## 7 instruction bootstrap
```
LDRT r5,[r6,#0x190]   E5B65190 # r5=REG_KEYINPUT
SWILS #5              9F050000 # C=0 or Z=1
LDR r1,[r5]           E5951000 # R1=keys
STB r1,[r6+1]         E4C61001 # write keys
AND r1,#0x300         E2110C03 # Z=L&R
STREQ r0,[r0]         04000130 # REG_KEYINPUT
LDRNET r0,[pc-0x148]  143F0148 # pseudo-BNE
```

## Box name bootstrap
- Bootstrap: 1F 09 18 03 02 FF (Box 1 name; THUMB) (まけねうい)
1. Setup key input
2. Write lower 8 bits
3. Loop unless L&R pressed
```
Box1: @ 02 4D 34 1D 05 DF 04 E0 (いぷゃへおkえl)
LDR r5,[pc,#8]  4D02 @ r5=REG_KEY_INPUT
ADD r4,r6,#4    1D34 @ r4=loop target
SWI #5          DF05
B Box3          E004
Box2: xx xx xx 30 01 00 04 (ぃぃぃぃあ え)
.space 3
.4byte 0x04000130 @ REG_KEYINPUT
Box3: @ 29 68 71 77 81 4F 04 E0 (るネムラゥぽえl)
LDR r1,[r5]     6829 @ r1=keys
STRB r1,[r6]    7031 @ write keys
LDR r3,[pc,#4]  4F81 @ r3=0x300
B Box5          E004
Box4: @ xx 00 03 00 00 (  う  )
.space 1
.4byte 0x00000300
Box5: @ 01 36 19 42 00 D0 20 47 (あょのぢ Vみび)
ADD r6,#1       3601
TST r1,r3       4219 @ Z=L&R
BEQ target      D000
BX r4           4720 @ loop to SWI
```
