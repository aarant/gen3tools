# Ruby (J) Docs

## Addresses
| Symbol | Address |
| ------ | ------- |
| RNG | 03004748 |
| gSaveBlock1 | 02025494 |
| gPlayerParty | 03004290 |
| mail | 02027FE0 |
| GiveMailToMon | 809F144 |
| GiveMailToMon2? | 0809F2FC |
| gMapHeader | 0202E588 |
| gUnknown_02029828 | 02029588 |
| gUnknown_03004870 | 030047A0
| bagItems | 020259f4 |
| GiveMailInput | 8087EC4 |
| playerRoomDecor | 02027b1c |


## Mail Trick glitch
- atkD2_tryswapitems does not check mail at 08027518
- mail struct: 9 u16 words, 8 character name, TID&SID, 2 byte species, 2 byte item ID
- mail ID is stored +5 bytes after BoxPokemon
1. Give mail to lead pokemon, mail slot 0
2. Enter a double battle. Use Thief on the first pokemon.
3. Take the mail from the second pokemon.
4. Give mail to the last 5 pokemon.
5. Give any item to the lead pokemon.
6. Repeatedly give the lead pokemon mail to clone its item.
To corrupt metatiles:
1. Take the lead's item.
2. Deposit it in the PC.
3. Give the lead mail.
To recover slot 0:
1. Take the lead's item.
2. Give the lead mail.
```
02027FE0
02028004
02028028
0202804C
02028070
02028094
020280B8
020280DC
02028100
02028124
02028148
0202816C
02028190
020281B4
020281D8
020281FC

0202a3bc
```
- PartyMenuTryGiveMonHeldItem
  - PartyMenuUpdateMonHeldItem (806BC0C?)
    - GiveMailToMon
    - 0xff accesses 202a3bc

- Mailbox_DoGiveMailPokeMenu
  - sub_808B020
    - sub_808B0C0
      - PartyMenuTryGiveMonMail -- only called when giving mail from the mailbox

- gUnknown_03004870 is a BackupMapLayout
- gUnknown_02029828 is the map
- map_copy_with_padding (copies main layout with padding)
- affect x: 3, y:26 route 110
- GetBehaviorByMetatileId
- attributes are u16s



gMapHeader: 0202e828 in US, 0x0202E588 in JP (JP is 672 bytes behind)


## Secret Base glitch
- secretBases: 0x2026e9c, decorations +0x12
- playerRoomDecor: 12 bytes at 02027b1c
- sub_8101848 in US, 0x80FC768 in JP?
- index: 0x020385ED base: 0x020385C8 (gUnknown_020388D0 on US)
- break 0x80FC78C
- read: 0x80F99A8?, sub_80FEABC? in US
- gStringVar1: 0x020231F0?
- gDecorations: 0x083C2A44
- description pointer = gDecorations+28*id+20
- 0x0202E668 -- where the decoration's pointer to its description is stored
- 0x8002E54 HandleExtCtrlCode -- Cannot use any code > 0x10!
- TVShows: 0x2027bcc?
