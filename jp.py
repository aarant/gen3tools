from seed import method1_mons, r_nature, seeds, rand, nature_map, dmg_seek, acc_seek
from pokemon import BoxMon, perms


def test_double_corrupt(pid, otId):  # Test double corruption of Mudkip
    mon = BoxMon()
    mon.personality = pid
    mon.otId = otId
    mon.sub(0).type0.species = 283
    mon.sub(0).type0.experience = 135
    mon.sub(0).type0.friendship = 70
    sub1 = mon.sub(1).type1
    sub1.moves[0] = 33
    sub1.moves[1] = 45
    sub1.pp[0] = 35
    sub1.pp[1] = 40
    sub2 = mon.sub(2).type2
    sub2.attackEV = 0x31
    sub2.hpEV = 0x10
    sub3 = mon.sub(3).type3
    sub3.metLocation = 16
    sub3.metLevel = 5
    sub3.metGame = 3
    sub3.pokeBall = 4
    sub3.otGender = 1
    mon.checksum = mon.calc_checksum()
    sum1 = mon.checksum
    mon.encrypt()
    mon.personality |= 0x40000000
    mon.decrypt()
    sum2 = mon.calc_checksum()
    mon.encrypt()
    mon.otId |= 0x40000000
    mon.decrypt()
    sum3 = mon.calc_checksum()
    if sum1 == sum2 == sum3 and mon.sub(3).type3.isEgg == 0:
        move = mon.sub(1).type1.moves[0]
        if move != 0x3110:
            mon.export()
        return move == 0x3110
    return False


def corruptible(pid, otId) -> bool:  # Test if corruption swaps EVs and Moves
    sub2 = perms[pid % 24][2]  # EVs
    pid2 = pid | 0x40000000
    sub1_p = perms[pid2 % 24][1]  # Attacks
    return test_double_corrupt(pid, otId) if sub1_p == sub2 else False


def mudkip_key(t):  # Key for ranking Mudkip PIDs
    i, pid, ivs = t
    nature = pid % 25
    if nature == 17:  # Quiet
        nature = 0
    elif nature == 16:  # Mild
        nature = 1
    elif nature == 19:  # Rash
        nature = 2
    else:
        nature = 3
    ivs = tuple(31-iv for iv in ivs)  # Prefer higher IVs
    prefer = (ivs[3], ivs[1], ivs[5], ivs[4], ivs[2], ivs[0])  # sa, at, sp, sd, de, hp
    # prefer = (ivs[4], ivs[1], ivs[3], ivs[5], ivs[2], ivs[0])  # sa, at, sp, sd, de, hp (old)
    return (nature,) + prefer + (i,)


def glitch_mudkip(seed, otId, cycle, limit=600):  # Print good mudkip candidates
    offset = 6018
    inp_offset = -3
    candidates = []
    for i, pid, ivs in method1_mons(seed, offset, limit):
        if corruptible(pid, otId):
            candidates.append((i, pid, ivs))
    candidates.sort(key=mudkip_key)
    for i, pid, ivs in candidates[:10]:
        print(f'{i+cycle+inp_offset} {pid:08x} {r_nature[pid % 25]} {ivs}')


def male_mons(seed, frame=0, limit=1000, threshold=127):  # Yield Wally's Ralts
    for i, base in enumerate(seeds(seed, frame, limit), frame):
        rng = rand(base)
        gender = 1
        while gender != 0:  # MON_MALE
            otId = next(rng) | (next(rng) << 16)
            pid = next(rng) | (next(rng) << 16)
            gender = 1 if threshold > (pid & 0xff) else 0
        value = next(rng)
        hp, at, de = value & 0x1f, (value & 0x3e0) >> 5, (value & 0x7c00) >> 10
        value = next(rng)
        sp, sa, sd = value & 0x1f, (value & 0x3e0) >> 5, (value & 0x7c00) >> 10
        yield i, pid, otId, (hp, at, de, sa, sd, sp)


def zigzag_key(t):
    i, pid, ivs = t
    # hp, at, de, sa, sd, sp = tuple(31-iv for iv in ivs)
    prefer = 0 if ivs[1] >= 26 else 1
    return prefer, i


def wally_zigzagoon(seed, cycle, limit=1000):
    offset = 2  # 1 frame skipped, the next is used
    candidates = []
    for i, pid, ivs in method1_mons(seed, offset, limit):
        candidates.append((i, pid, ivs))
    candidates.sort(key=zigzag_key)
    for i, pid, ivs in candidates[:10]:
        print(f'{i+cycle-offset} {pid:08x} {r_nature[pid % 25]} {ivs}')


def ralts_key(t):
    i, pid, ivs = t
    allowed = {nature_map[name] for name in ('lonely', 'hasty', 'mild', 'gentle')}
    nature = 0 if (pid % 25) in allowed else 1
    prefer = 0 if nature == 0 and ivs[0] <= 3 and ivs[2] <= 5 else 1
    return prefer, i


def ralts_seek(seed, cycle, limit=600):
    offset = 2
    candidates = []
    for i, pid, _, ivs in male_mons(seed, offset, limit):
        candidates.append((i, pid, ivs))
    candidates.sort(key=ralts_key)
    for i, pid, ivs in candidates[:10]:
        print(f'{i+cycle-offset} {pid:08x} {r_nature[pid % 25]} {ivs}')

# 0cbe8210 9b1c
# 8975 b2a8c6e9 quiet (17, 31, 3, 23, 16, 26)

# 1981bcf6 2aed
# 8822 1ea3ba4e quiet (25, 23, 22, 19, 31, 31)

# 9dd097ca 54b6 9dd054b6
# 8762 b5d405b7 mild (25, 21, 6, 21, 26, 31)

# abefc4e8 8274 abef8274
# 8750 3e239481 rash (16, 31, 24, 30, 5, 23)


if __name__ == '__main__':
    # tid = 0x54ab
    # seed = 0x38033fcc
    # otId = ((seed >> 16) << 16) | tid
    # print(f'{seed:08x} {tid:04x} {otId:08x}')
    # glitch_mudkip(seed, otId, 2726)
    # ralts_seek(0xda3b0abd, 30279, 60*4)
    # nocrit_seek(0xf6f7bdf80, limit=20)
    acc_seek(0xfb299337, move_acc=80, limit=20)
    print()
    dmg_seek(0x8a5d8b46, limit=20)
