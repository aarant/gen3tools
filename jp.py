import math

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

def species_corruptible(pid: int) -> bool:  # Whether corruption swaps EVs and species
    sub2 = perms[pid % 24][2]  # EVs
    pid2 = pid | 0x40000000
    sub0_p = perms[pid2 % 24][0]  # Growth
    return sub2 == sub0_p


def mudkip_key(t):  # Key for ranking Mudkip PIDs
    i, pid, ivs = t
    nature = pid % 25
    if nature == 16:  # Mild
        nature = 1
    elif nature == 19:  # Rash
        nature = 0
    else:
        nature = 2
    ivs = tuple(31-iv for iv in ivs)  # Prefer higher IVs
    prefer = (0 if ivs[3] < 2 else 10, ivs[1], ivs[5], ivs[2], ivs[4], ivs[0])  # sa, at, sp, de, sp, hp
    return (nature,) + prefer + (i,)


def glitch_mudkip(seed, otId, cycle, limit=600):  # Print good mudkip candidates
    offset = 6018  # Approximate number of cycles from ID generation to Mudkip
    offset = 8606-2641+3  # 5968, 1 character name
    inp_offset = -3
    candidates = [(i, pid, ivs) for i, pid, ivs in method1_mons(seed, offset, limit) if species_corruptible(pid)]
    # candidates = [(i, pid, ivs) for i, pid, ivs in method1_mons(seed, offset, limit) if corruptible(pid, otId)]
    candidates.sort(key=mudkip_key)
    print('Cycle PID      Nature  HP  AT  DE  SA  SD  SP')
    for i, pid, ivs in candidates[:10]:
        ivs = ', '.join(f'{iv:2d}' for iv in ivs)
        print(f'{i+cycle+inp_offset:5d} {pid:08x} {r_nature[pid % 25]:7} {ivs}')
    return candidates[0]


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

# V4:   8fd82cd8 Rash   (12, 30, 23, 31,  5, 10)

# Seed: f3423004->E4E80A27 ID: 283e f342283e
# Cycle PID      Nature  HP  AT  DE  SA  SD  SP
#  8688 81ee947c rash    22, 30,  2, 30, 10, 27

# Seed: d1e63191->A943A930 ID: 88d3 d1e688d3
# Cycle PID      Nature  HP  AT  DE  SA  SD  SP
#  8951 2b420c53 rash    22, 28, 11, 28, 31,  7

# Seed: b839f665->50DF0F74 ID: b2c7 b839b2c7
# Cycle PID      Nature  HP  AT  DE  SA  SD  SP
#  9115 8370b91c mild    30, 29, 28, 30, 16, 30

# Seed: b267eef8->6CE0B00B ID: 0152 b2670152
# Cycle PID      Nature  HP  AT  DE  SA  SD  SP
#  8839 89ec0772 rash    26, 26, 27, 30,  1, 31

# Seed: 937cc3e8->3D407A3B ID: cbc2 937ccbc2
# 8621 2807214c mild    21, 30, 27, 30, 16,  4


def find_best_tid():
    global print

    print('TID  Cycle PID      Nature  HP  AT  DE  SA  SD  SP')
    old_print, print = print, lambda *args: None
    best = None
    for initial in tried_tids:
        for off in range(-1, 1+1):
            tid = initial + off
            if tid in tried_tids:
                continue
            seed = next(seeds(tid, 590))
            otId = ((seed >> 16) << 16) | tid
            new_best = glitch_mudkip(seed, otId, 0)
            i, pid, ivs = new_best
            ivs = ', '.join(f'{iv:2d}' for iv in ivs)
            old_print(f'{tid:04X} {i:5d} {pid:08x} {r_nature[pid % 25]:7} {ivs}')
            if best is None:
                best = new_best
                continue
            l = [best, new_best]
            l.sort(key=mudkip_key)
            new_best = l[0]
            if best != new_best:
                old_print('^')
            best = new_best
    print = old_print


if __name__ == '__main__':
    tried_tids = {0x0153, 0X283E, 0x71dd, 0xb5c8, 0x0331, 0x4c85, 0x7d5d, 0xcbce,  # No extra buttons
                  0x0670, 0x4ba3, 0x88cd, 0xd18a, 0x1ac9, 0x640d, 0xb2c1, 0x015c,
                  0x71e3, 0xb5ce, 0x0337, 0x4c7b, 0x7d63, 0xcbc4, 0x0666, 0x4ba9,  # l
                  0x88D3, 0xD190, 0x1ACF, 0x6413, 0xb2c7, 0x0152, 0x41b0, 0x8a3e,
                  0x71e2, 0xb5c9, 0x0330, 0x4c86, 0xcbc9, 0x066f, 0x4ba8, 0x88ce,  # L&R
                  0xD184, 0x1aca, 0xb2c2, 0x0155, 0x41a3, 0x8a3b, 0xd247, 0x1b9f,
                  0x71EC, 0xB5C4, 0x032C, 0x4C7D, 0x7d64}  # L&R&S
    cycle, seed, tid = (2628, 0x937cc3e8, 0xcbc2)
    test_seed = next(seeds(tid, 590))
    seed = test_seed
    if tid in tried_tids:
        print(f'TID 0x{tid:04X} already tried!')
        quit()
    otId = ((seed >> 16) << 16) | tid
    seed2 = list(seeds(seed, limit=2))[-1]
    print(f'Seed: {seed:08x}->{seed2:08X} ID: {tid:04x} {otId:08x}')
    glitch_mudkip(seed, otId, cycle)

    # 616 frames between
    # diff is
    # print(30149-616)
