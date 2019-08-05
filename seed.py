from itertools import islice

from pokemon import BoxMon


def seeds(seed=0, frame=None, limit=2**32):
    """ Yields successive seeds up to a limit.

    Args:
        seed (int): Seed to start on. Defaults to 0.
        frame (int): Frames to skip. Defaults to None.
        limit (int): Number of seeds to produce. Defaults to 2**32.
    >>> list(seeds(limit=4))
    [0, 24691, 3917380458, 1383151765]
    """
    if frame and seed == 0:  # Use fast seed calculation
        seed = seed_at(frame)
    elif frame and seed != 0:  # Need to advance manually
        for _ in range(frame):
            seed = 0xffffffff & seed * 0x41c64e6d + 0x6073
    for _ in range(limit):
        yield seed
        seed = 0xffffffff & seed * 0x41c64e6d + 0x6073


def seed_at(frame: int) -> int:
    """ Get the seed that would occur on a frame.

    This only works for a base seed of zero.

    Args:
        frame (int): Frame to find.

    Returns:
        int: Seed that occurs on that frame.
    >>> seed_at(800) == list(seeds(frame=800, limit=1))[0]
    True
    >>> seed_at(0) == 0 == seed_at(2**32)
    True
    >>> (seed_at(2**32-1)*0x41c64e6d + 0x6073) % 2**32
    0
    """
    m = 2**32
    a = 0x41c64e6d
    b = 0x6073
    # I'm unable to find the webpage I found this method on, but it works.
    res = (a-1)*m
    return (((pow(a, frame, res)-1) % res)//(a-1)*b) % m
    return ((a**frame-1)//(a-1)*b) % m


def cycles_to(seed: int):
    """ Find the number of RNG cycles needed to get a seed, starting from 0.

    Args:
        seed (int): Seed to match.

    Returns:
        int: The frame that seed occurs on.
    >>> cycles_to(0)
    0
    >>> cycles_to(0x6073)
    1
    """
    for i, seed2 in enumerate(seeds()):
        if seed2 == seed:
            return i


def choose_land_index(rng):  # pick a wild mon index
    rand = next(rng) % 100
    if rand < 20:
        return 0
    elif 20 <= rand < 40:
        return 1
    elif 40 <= rand < 50:
        return 2
    elif 50 <= rand < 60:
        return 3
    elif 60 <= rand < 70:
        return 4
    elif 70 <= rand < 80:
        return 5
    elif 80 <= rand < 85:
        return 6
    elif 85 <= rand < 90:
        return 7
    elif 90 <= rand < 94:
        return 8
    elif 94 <= rand < 98:
        return 9
    elif rand == 98:
        return 10
    else:
        return 11


def wild_mons(seed=0, frame=0, limit=1000, diff=False, bike=False, rate=20, slots=None):
    """ Yield (frame, seed, pid) tuples for wild pokemon encounters.

    Seed is the value of the RNG at the frame before the tile transition.

    Args:
        seed (int): Starting value for RNG. Defaults to 0.
        frame (int): Frames to skip. Defaults to 0.
        limit (int): Limit of frames to search through. Defaults to 1000.
        diff (bool): If the previous and current metatiles differ. Defaults to False.
        bike (bool): If a bike is being ridden. Defaults to False.
        rate (int): Encounter rate of area.
    """
    offset = 2  # 1 frame is skipped, the next is used
    rate *= 16
    rate = (80 * rate // 100) if bike else rate
    rate = min(rate, 2880)
    for i, base in enumerate(seeds(seed, frame, limit), frame):
        rng = (r >> 16 for r in seeds(base, offset))
        if diff and not next(rng) % 100 < 60:  # Global encounter check
            continue
        elif not next(rng) % 2880 < rate:  # Local encounter check
            continue
        slot = choose_land_index(rng)
        if slots is not None and slot not in slots:
            continue
        level = next(rng) % 10  # TODO: Replace with range
        nature = next(rng) % 25  # PickWildMonNature
        first = True
        pid = 0
        while first or pid % 25 != nature:  # CreateMonWithNature
            low = next(rng)
            high = next(rng)
            pid = (high << 16) | low
            first = False
        yield i, base, pid


def method1_mons(seed=0, frame=0, limit=1000):
    """ Yields (frame, pid, evs) tuples for method 1 pokemon.

    Args:
        seed (int): Starting value for RNG. Defaults to 0.
        frame (int): Frames to skip. Defaults to 0.
        limit (int): Limit of frames to search through. Defaults to 1000.
    """
    for i, base in enumerate(seeds(seed, frame, limit), frame):
        rng = [r >> 16 for r in seeds(base, limit=4)]
        pid = (rng[1] << 16) | rng[0]
        hp, at, de = rng[2] & 0x1f, (rng[2] & 0x3e0) >> 5, (rng[2] & 0x7c00) >> 10
        sa, sd, sp = rng[3] & 0x1f, (rng[3] & 0x3e0) >> 5, (rng[3] & 0x7c00) >> 10
        yield i, pid, (hp, at, de, sa, sd, sp)


def test_double_corrupt(pid: int, otId: int) -> bool:
    """ Determine if the pid, OTId pair can be used for double corruption.

    Args:
        pid (int): PID of pokemon to corrupt.
        otId (int): OTId of trainer.

    Returns:
        bool: True if the pair can be used, False otherwise.
    """
    box_mon = BoxMon()
    box_mon.personality = pid
    box_mon.otId = otId
    box_mon.sub(0).type0.species = 308
    box_mon.sub(0).type0.experience = 2195
    box_mon.sub(0).type0.friendship = 70
    sub1 = box_mon.sub(1).type1
    sub1.moves[0] = 33
    sub1.moves[1] = 253
    sub1.moves[2] = 185
    sub1.pp[0] = 35
    sub1.pp[1] = 10
    sub1.pp[2] = 20
    sub2 = box_mon.sub(2).type2
    sub2.attackEV = 22
    sub2.hpEV = 8
    sub3 = box_mon.sub(3).type3
    sub3.metLocation = 28
    sub3.metLevel = 14
    sub3.metGame = 3
    sub3.pokeBall = 2
    sub3.otGender = 1
    sub3.unk = 977594907
    box_mon.checksum = box_mon.calc_checksum()
    sum1 = box_mon.checksum
    box_mon.encrypt()
    box_mon.personality |= 0x40000000
    box_mon.decrypt()
    sum2 = box_mon.calc_checksum()
    box_mon.encrypt()
    box_mon.otId |= 0x40000000
    box_mon.decrypt()
    sum3 = box_mon.calc_checksum()
    if sum1 == sum2 == sum3 and box_mon.sub(3).type3.isEgg == 0:
        box_mon.encrypt()
        return True
    return False


def berry_master(item=153, frame=800, limit=2**16):  # Finds frames for collecting pomeg berries
    mod = item-153
    for i, seed in enumerate(seeds(frame=800, limit=limit), frame):
        if (seed >> 16) % 10 == mod:
            print('{:08x} at {}'.format(seed, i))


def find_good_sweep():  # Find good quick claw/OHKO sweeps
    streaks = {}
    max_streak = 0
    seed = seed_at(1800)
    for frame in range(1800, 2**18):  # Explore low numbers of frames right now
        streak = 0
        seed1 = seed
        while True:
            seed2 = 0xffffffff & seed1 * 0x41c64e6d + 0x6073
            turn, dmg = seed1 >> 16, seed2 >> 16
            # Quick Claw needs to activate and OHKO must hit
            if turn < 0x3333 and (dmg % 100 + 1) <= 30:
                streak += 1
                if streak > 2:
                    pass
                seed1 = 0xffffffff & seed2 * 0x41c64e6d + 0x6073
            else:
                break
        if streak > 2:
            print('{} found at frame {}, second {} seed {:08x}'.format(streak, frame, round(frame/60, 1), seed))
        if streak > max_streak:
            max_streak = streak
        if streak > 4:
            streaks[frame] = streak
        seed = 0xffffffff & seed * 0x41c64e6d + 0x6073
    print('Done')
    print(streaks)


def battle_seeds(seed=0, frame=0, limit=1000):
    yield from islice(seeds(seed, frame*2, limit*2), 0, None, 2)


def ever_grande_glitch():  # Show all the 0x40 corruptions possible with pomeg glitch
    corruptions = [0x4b, 0x3f, 0x33, 0x27]
    offsets = []
    start = 0x0202a888
    while start > 0x02026000:
        if 0x02026c50 < start < 0x02026f00:
            for c in corruptions:
                offsets.append(start+c)
        start -= 100
    print(' '.join('%08x' % x for x in offsets))


nature_map = {'hardy': 0, 'lonely': 1, 'brave': 2, 'adamant': 3, 'naughty': 4, 'bold': 5, 'docile': 6,
              'relaxed': 7, 'impish': 8, 'lax': 9, 'timid': 10, 'hasty': 11, 'serious': 12,
              'jolly': 13, 'naive': 14, 'modest': 15, 'mild': 16, 'quiet': 17, 'bashful': 18,
              'rash': 19, 'calm': 20, 'gentle': 21, 'sassy': 22, 'careful': 23, 'quirky': 24}
r_nature = {v: k for k, v in nature_map.items()}

gender_thresholds = {'1:7': 225, '1:3': 191, '1:1': 127, '3:1': 63, '7:1': 31}


# Help display
# Absolute lowest frame possible is around 650 ish
# Banette offset is 267 from target frame
# Oddish offset is 267 from target frame
otId = 0x0d59efe7
print('RNG is at address 03005D80')
print('RNG cycle count at 020249c0')
print('gRandomTurnNumber is at 02024330')

if __name__ == "__main__":
    import doctest
    doctest.testmod()
