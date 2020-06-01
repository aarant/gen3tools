.text
.syntax unified
.thumb
.include "asm/event.inc"
.include "asm/map.inc"

lanetteScript: @ 0203d000
  lock
  faceplayer
  checkflag 0x13C @ FLAG_RECEIVED_OLD_SEA_MAP
  goto_if 1, haveMap
  msgbox text1, MSGBOX_YESNO
  compare 0x800D, 1 @ VAR_RESULT
  goto_if_eq answerYes
  msgbox text2
  release
  end
answerYes:
  msgbox text3
  gotonative BattlePatch+1
  faceplayer
  .byte 0x26
  .2byte 0x800D, 0xB4 @ specialvar VAR_RESULT, GetBattleOutcome
  compare 0x800D, 1 @ VAR_RESULT, B_OUTCOME_WON
  goto_if_eq battleWon
  msgbox text5
  release
  end
battleWon:
  msgbox text4
  @ giveitem_std OLD_SEA_MAP
  setorcopyvar 0x8000, 376
	setorcopyvar 0x8001, 1
	callstd 0
  setflag 0x860+0x76 @ FLAG_ENABLE_SHIP_FARAWAY_ISLAND
	setflag 0x13C @ FLAG_RECEIVED_OLD_SEA_MAP
haveMap:
  msgbox text6
  @ warpteleport 0x0005, 12, 0, 0
  release
  end
text1: .string "Hey!\rDid you enjoy the TAS?\rI put a lot of work\ninto it!\rFor one last trick.\nWant to have a battle?"
text2: .string "OK! Come back anytime!"
text3: .string "\xfcさ6あAlright! Here goes..\rI wonder..\nis luck on your side?"
text4: .string "Great job!\nHere. Take this!"
text5: .string "Better luck next time!"
text6: .string "That \xfcあえOLD SEA MAP\xfcあい..\rIt was available many\nyears ago.\rYou deserve it!"

.align 1
BattlePatch:
  push {lr}
  push {r2, r3, r4}
  ldr r1, BattleSetup_ConfigureTrainerBattle
  adr r0, battleData
  bl _call_via_r1
  ldr r1, BattleSetup_StartTrainerBattle
  bl _call_via_r1
  ldr r0, song
  ldr r1, PlayMapChosenOrBattleBGM
  bl _call_via_r1 @ play music
  ldr r0, battleTask
  movs r1, #16
  movs r2, #4
_bpscan: @ scan the task list and change transition type
  cmp r1, #0
  beq _bp1
  strh r2, [r0]
  adds r0, #40
  subs r1, #1
  b _bpscan
_bp1:
  ldr r0, gBattleTypeFlags
  ldr r1, [r0]
  movs r2, #1
  lsls r2, #27
  orrs r1, r2
  str r1, [r0] @ OR with SECRET_BASE
  ldr r1, gSaveBlock1Ptr
  ldr r1, [r1]
  ldr r0, baseOffset
  adds r1, r0
  adr r0, baseData
  movs r2, #7 @ size of baseData in HW
  swi 11 @ copy trainer name, model, ID to base
  adds r1, #0x34 @ party
  adr r0, secretBaseParty
  movs r2, #48 @ size up to levels
  swi 11 @ copy party except levels
  ldr r0, playerParty
  movs r2, #6 @ counter
  movs r3, #20 @ default level
_levelscan: @ Scan player's levels and match them
  cmp r2, #0
  beq _levelset
  ldrb r4, [r0]
  cmp r3, r4
  bhi _bp4
  movs r3, r4
_bp4:
  adds r0, #100 @ 100 bytes per pokemon
  subs r2, #1
  b _levelscan
_levelset:
  subs r3, #5
  adds r1, #96
  adds r2, r1, #6
_bp5:
  cmp r1, r2
  beq _bp6
  strb r3, [r1]
  adds r1, #1
  b _bp5
_bp6:
  movs r0, #1
  pop {r2, r3, r4}
  pop {r1}
_call_via_r1:
  bx r1
.align 2
BattleSetup_ConfigureTrainerBattle: .4byte 0x080B0D1C+1
PlayMapChosenOrBattleBGM: .4byte 0x0806E0F4+1
song: .4byte 471 @ 508
battleTask: .4byte 0x03005B60+10
BattleSetup_StartTrainerBattle: .4byte 0x080B10CC+1
playerParty: .4byte 0x02024190+84 @ level
gBattleTypeFlags: .4byte 0x02022C90
gSaveBlock1Ptr: .4byte 0x03005aec
baseOffset: .4byte 0x1A9C
battleData:
  .byte 3 @ TRAINER_BATTLE_SINGLE_NO_INTRO_TEXT
  .2byte 1024, 1
  .4byte 0
.align 2
baseData: .byte 0x00, 0x10
trainerName: .byte 0xc7, 0xd9, 0xe6, 0xe6, 0xe4, 0xff, 0xff @ merrp
trainerID: .4byte 4
.align 2
secretBaseParty:
  .4byte 1, 1, 1, 1, 1, 1 @ PIDS
  .2byte 161, 246, 126, 352 @ Tri Attack, Ancientpower, Fire Blast, Water Pulse
  .2byte 225, 189, 202, 104 @ Dragonbreath, Mud Slap, Giga Drain, Double Team
  .2byte 188, 282, 12, 14 @ Sludge Bomb, Knock Off, Guillotine, Swords Dance
  .2byte 149, 8, 168, 347 @ Psywave, Ice Punch, Thief, Calm Mind
  .2byte 205, 111, 214, 156 @ Rollout, Defense Curl, Sleep Talk, Rest
  .2byte 118, 309, 322, 135 @ Metronome, Meteor Mash, Cosmic Power, Softboiled
  .2byte 176, 334, 327, 352, 213, 36 @ Togetic, Flygon, Crawdaunt, Grumpig, Shuckle, Clefable
  .2byte 174, 179, 183, 142, 219, 200 @ Starf Berry, Brightpowder, Quick Claw, Sitrus Berry, Shell Bell, Leftovers
