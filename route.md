# Game Start
- YOLO TID since it is the lower 16 bits of an ARM instruction and thus can't predict whether it will be valid.
- You need to name your trainer (I  v). That's two spaces in between the I and v.
- Nickname Mudkip (mFloyLRo  ). Again, two spaces on the end.

# Mauville City
- Head east to Route 119.

# Route 119 & 123
- Fight the double battle, avoid all stationary trainers.
- Talk to Steven, bike east to Route 123.
- Enter Route 123, avoid double battle & spinner.
- Pick up 2 Pomeg berries from the leftmost patch.
- Teleport to Mauville, head west to Verdanturf/Route 116.

# Route 116
- Pick up HP Up
- Head west to Rustboro

# Rustboro
- Trade Ralts for DOTS the Seedot.
- Head south, pick up Bullet Seed near the Flower Shop for Seedot?

# Petalburg Woods
- Use HP Up on Seedot. You'll then need to KO 7 Shroomish and 6 Poochyena to get (17 HP 6 AT) on Seedot
- Alternatively, for a more RNG-based strategy, you can KO Marill on Route 104, which give 2 HP EVs each.
- Poison Marshtomp and heal it at 1 HP.
- Teleport back to setup Glitzer Popping.

# Glitzer Popping
1. Order party as KOed Abra, Marshtomp, Seedot.
2. Save your game in grass.
3. Enter a wild battle, switch to Seedot and flee.
4. Deposit Seedot in Box 2 Slot 24.
5. Use Pomeg Berry on Marshtomp.
6. Enter a battle, open the party menu, view Marshtomp's summary, exit, and press up 3 times to corrupt Seedot.
7. Flee, you will white out and return to the teleport point.
8. Open the PC and check Box 2.
   - If nothing visibly changed, repeat from 6.
   - If DOTS became a Bad Egg, soft reset and repeat from 3.
   - If DOTS became an Egg, check the ball it's in. If it's a Premier Ball, soft reset and repeat from 3.
   - If it's in a Nest Ball, congrats, you got it!
   - Chance to corrupt is 1/32.

# ACE Setup
Make sure the following nicknamed pokemon are at these slots in the PC:

All nicknames should end in two spaces.

Box 12 Slot 01: Mudkip named (mFloyLRo  )

Box 12 Slot 11: Any named (m”RoLT-n  ) -- Note that this is a *right* quotation mark that opens to the left.

Box 12 Slot 21: Any named (YN?nFNRo  )

Box 13 Slot 01: Any named (z ?n?E0q  )

- Withdraw the Egg into your third party slot.
- If you don't want to scrap the run if this fails, save here.
- Hatch the Egg by riding the Mach Bike.
- When the Egg hatches, if your TID/SID is good the ACE will trigger and put you into the Hall of Fame. Congrats!

The chance of your TID/SID working is hard to quantify. In order to work, the ARM instruction formed by them must be
both legal and harmless. The chance of it being harmless if legal is at least 50%. The chance of it being legal is
probably around 80%. I'm estimating that a random TID & SID will work about 60% of the time.

If your game crashes when hatching the Egg, and you want to continue:
- Reload your save with the Egg.
- Set up your PC as:

Box 11 Slot 30: Any named (   l   l  ) (3 spaces, l, 3 spaces, l, 2 spaces)

Box 12 Slot 10: Mudkip named (mFloyLRo  )

Box 12 Slot 20: Any named (m”RoLT-n  ) -- Note that this is a *right* quotation mark that opens to the left.

Box 12 Slot 30: Any named (YN?nFNRo  )

Box 13 Slot 10: Any named (z ?n?E0q  ) -- Zero, not o

- Hatch the Egg, but try and save as close to the hatching as possible.
- Chance to work is now 1/32 and completely dependent on you getting the right memory layout.
