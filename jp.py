from seed import method1_mons, r_nature, seeds, rand, nature_map, dmg_seek, acc_seek, wild_mons
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
        nature = 0
    else:
        nature = 2
    ivs = tuple(31-iv for iv in ivs)  # Prefer higher IVs
    prefer = (0 if ivs[3] < 2 else 10, ivs[1], ivs[5], ivs[2], ivs[4], ivs[0])  # sa, at, sp, de, sp, hp
    # prefer = (ivs[4], ivs[1], ivs[3], ivs[5], ivs[2], ivs[0])  # sa, at, sp, sd, de, hp (old)
    return (nature,) + prefer + (i,)


def glitch_mudkip(seed, otId, cycle, limit=600):  # Print good mudkip candidates
    offset = 6018  # Approximate number of cycles from ID generation to Mudkip
    offset = 8606-2641+3  # 5968, 1 character name
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


# abefc4e8 8274 abef8274 <- old run
# 8750 3e239481 rash (16, 31, 24, 30, 5, 23)

# new run
# 8d09cd33 015a 8d09015a
# 8823 224ab97e rash (11, 29, 18, 30, 10, 13)

# a81e3fce 6198 a81e6198
# 8793 9f25f709 quiet (23, 28, 11, 30, 12, 17)

# 1445cb24 4c79 14454c79
# 8778 22d07e1f rash (17, 31, 15, 29, 4, 10)

# 9c87095d 4c86 9c874c86 (1 r press)
# 8772 19af1896 rash (22, 31, 12, 30, 23, 29)

# a8647611 0153 a8640153 (l, r)
# 8695 8fd82cd8 rash (12, 30, 23, 31, 5, 10)

b = ['81 94 23 3e 74 82 ef ab 57 ff ff ff ff ff 00 08',
     '4c 7d 01 02 0f 00 00 ea ff ff 00 00 e2 91 00 00',
     'f7 10 ca 85 f3 16 cc 95 f5 16 cc 95 f5 06 49 34',
     '05 f5 27 9e f5 16 cc 95 0c 16 99 94 48 16 fb 95',
     'fa 13 c6 80 e9 17 7b 95 b3 30 cc 95 f5 83 cc 95']

def pomeg_corrupt(addr, pid=0, tid=0):
    offset = 4 + 4 + 10 + 1 + 1 + 7 + 1 + 2 + 2
    sub_length = 3*4
    egg_offset = 1 + 1 + 2
    pos = perms[pid % 24][3]
    egg_addr = addr + offset + pos*sub_length + egg_offset
    return egg_addr


if __name__ == '__main__':
    # tid = 0x54ab
    # seed = 0x38033fcc
    # otId = ((seed >> 16) << 16) | tid
    # print(f'{seed:08x} {tid:04x} {otId:08x}')
    # glitch_mudkip(seed, otId, 2726)
    # for i in range(10):
    #     addr = 0x0202A52C-100*i
    #     egg_addr = pomeg_corrupt(addr)
    #     print(f'{addr:08x} {egg_addr:08x}')
    # tried = [0xb5ca, 0x0334, 0x4c83, 0x7d5c, 0xcbc8, 0x066b, 0x4ba9, 0x88d4,
    #          0xd18c, 0x1aca, 0x6409, 0xb2bc, 0x0152, 0x41ae, 0x8a37, 0xd24e,
    #          0x71e4, 0x71ea, 0xb5c0, 0x032a, 0x4c79, 0x71e3, 0xb5be, 0x0337,
    #          0x4c7b, 0x7d63, 0xcbc4, 0x0666, 0x88d3, 0xd180, 0x1acf, 0x6413,
    #          0x71e2, 0xb5c9, 0x0330, 0x4c86, 0x7d5d, 0xcbc9, 0x066f, 0x4ba8,
    #          0x88ce, 0x640d, 0xb2c2, 0x0155, 0x41a3, 0x8a3b, 0xd247, 0x1b9f,
    #          0xb5c6, 0x0339, 0x4c7d, 0x7d66, 0xcbc1, 0x0672, 0x4b9f, 0x88cb,
    #          0xd18f, 0x1acd, 0x6404, 0xb2c5, 0x0153, 0x41ad, 0x8a38, 0xd250,
    #          0xb5c7, 0x4c84, 0xcbcd, 0x4ba2, 0x88cc, 0xd189, 0x1ac8, 0x640c,
    #          0x032f, 0xcbc7, 0x0668, 0x4ba5, 0x88d1, 0xd185, 0x1ad3, 0x640a,
    #          0x0336, 0xcbca, 0x88c8, 0xd188, 0x014c, 0x41a9, 0x8a40, 0xd24c]
    # wally_zigzagoon(0x3a9bffd7, 29746)
    # print()
    # ralts_seek(0xf11aa2d9, 30068)
    for i in range(10):
        addr = 0x0202A52C-100*i
        egg_addr = pomeg_corrupt(addr)
        print(f'{addr:08x} {egg_addr:08x}')
