""" Tools for Gen 3 Arbitrary Code Execution (ACE). """
import struct
from seed import seeds, battle_seeds, method1_mons, wild_mons, r_nature, rand
from pokemon import perms, BoxMon, r_names


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


EVS = ('hpEV', 'attackEV', 'defenseEV', 'speedEV', 'spAttackEV', 'spDefenseEV')


ENC_FRAME = 700  # Practical lower bound for encounters


def glitch_move(otId: int, pairs):
    """ Yield (frame, pid) tuples for glitch move pokemon.

    Args:
        otId (int): Full 32-bit trainer id.
        pairs: Iterable of (i, pid) pairs.
    """
    for i, pid in pairs:
        sub2 = perms[pid % 24][2]  # EVs position
        pid2 = pid | 0x40000000
        sub1_p = perms[pid2 % 24][1]
        if sub1_p == sub2:  # Attacks is where EVs was, effectively swapping them
            if test_double_corrupt(pid, otId):  # Double corruption possible
                yield i, pid


def corruptible(pid: int, otId: int) -> bool:  # Whether a pid is corruptible
    sub2 = perms[pid % 24][2]  # EVs position
    pid2 = pid | 0x04000000
    sub1_p = perms[pid2 % 24][1]
    if sub1_p == sub2:  # Attacks is where EVs was
        return test_double_corrupt(pid, otId)
    return False


# Yields bootstrap pokemon
def stage_2(otId: int, address: int, pairs, sub=0, script=3, a1=0, a2=None, a3=None):
    # Pack in priority, address, n arguments, and next script in order
    raw = struct.pack('<BIBBB', script, address, a1, a2 if a2 else 0, a3 if a3 else 0)
    w0, w1 = struct.unpack('<II', raw)  # Unpack into two 32 bit words
    for i, pid in pairs:
        if perms[pid % 24][2] != sub:  # EV substruct must be in proper position
            continue
        mon = BoxMon()
        mon.personality = pid
        mon.otId = otId
        mon.secure.raw[sub*3] = w0  # Set first and second words
        mon.secure.raw[sub*3+1] = w1
        mon.decrypt()
        sub2 = mon.sub(2).type2
        if a2 is not None and sub2.cool != 0:  # Decrypted COOL must be 0
            continue
        elif a3 is not None and sub2.beauty != 0:  # Decrypted BEAUTY must be 0
            continue
        evs = tuple(getattr(sub2, e) for e in EVS)
        if sum(evs) > 510:
            continue
        yield i, pid, sum(evs), evs


# Yields bootstrap pokemon for nicknames
# HP AT DF SP SA SD CO BE
# SP DF AT HP BE CO SD SA
def bootstrap_names(otId: int, pairs):
    a1, a2, a3 = 0, None, None
    for sub in range(1):  # Try each substruct
        b1215 = 0x02030400-sub*3*4-6*4  # Address of *nickname*
        b101 = b1215 - (14 + 11 * 30) * 80
        for pos in range(30*10):
            address = b101+pos*80
            for i, pid, total, evs in stage_2(otId, address, pairs, sub, 31, a1, a2, a3):
                yield total, i, pid, evs, address, pos


# Opcodes available in ARM mode with nicknames
# Need to find a way back into THUMB code
# B
# ALU operations
# Can only use rd = 10,11,12,13,14, prefer 12 & 13
# ADC both
#   rn, no: n != 0, 15; yes: n != 7, 9
# SBC both, only odd shifts
# RSC no, n != 15
# MOV n = 0
# BIC both (bit clear)
# MVN no, n = 0
# Memory operations
# Cannot use PLD
# Must be Up; add to base
# if B=1 & T=1: no STR, n != 15
# if B=0, T=1: if L=1: n != 7, 9 else n != 0
# rd = 10,11,12,13,14, prefer 12 & 13
# Halfword memory
# Must be Up
# if I=0, P=1,W=1, if L=1: n != 7, 9 else n != 0, 15
# rd = 10,11,12,13,14, prefer 11,12,13,14
# STRH: rm != 7, 9
# LDR (double word)
# LDRH: rm != 7, 9
# LDR (signed extended byte)
# Block data transfer
# Must be Up
# if S=0,W=0: Invalid
# if S=0,w=1: if L=0: n != 0, 15 else n != 7, 9
# if S=1,W=1: L=0, n != 15
# Can only pop/push register subsets


def rng_ids(seed: int, tid: int, limit=70):  # Yields full trainer ids from a seed and TID
    # TODO: Add in offset
    for i, s in enumerate(seeds(seed, limit=70)):
        yield i, ((s >> 16) << 16) | tid


# HP: route 111, route 116
# AT: Pickup, route 106, route 111, route 114
# DE: route 115, route 118
# SP: route 114


def method1_key(t):  # Used to sort the best mudkips
    nature = t[1] % 25
    if nature == 17:  # Quiet
        nature = 0
    elif nature == 16:  # Mild
        nature = 1
    elif nature == 19:  # Rash
        nature = 2
    else:
        nature = 3
    ivs = tuple(31-i for i in t[2])  # Prefer higher IVs
    prefer = (ivs[3], ivs[1], ivs[5], ivs[4], ivs[2], ivs[0])  # sa, at, sp, sd, de, hp
    return (nature,) + prefer + (t[0],)


def analyze_id(seed: int, otId: int, cycle: int):
    mudkips = list(method1_mons(seed, MUDKIP, 1000))
    mudkips.sort(key=method1_key)
    print('Mudkip')
    for i, pid, evs in mudkips[:5]:
        can_corrupt = corruptible(pid, otId)
        c_str = '!' if can_corrupt else ''
        print(f'{i+cycle:>5} {r_nature[pid % 25]} {pid:08x}{c_str} {evs}')
    print('Bootstrap')
    triples = list(wild_mons(seed, MUDKIP+10000, 60*60*60))
    pairs = [(t[0], t[-1]) for t in triples]
    min_total = 100
    for total, i, pid, evs, address, pos in bootstrap_names(otId, pairs):
        if total < min_total:
            min_total = total
            box, index = divmod(pos, 30)
            print(f'{i+cycle:>6} {pid:08x} {total} {evs} {address:08x} Box {box+1} {index+1}')
    triples = list(wild_mons(seed, MUDKIP+10000, 60*60*60, slots={3}))
    pairs = [(t[0], t[-1]) for t in triples]
    print(f'Abra/glitch: {len(list(glitch_move(otId, pairs)))} PIDs')


def explore_ids(seed, tid, cycle, limit=70):
    mudkips = list(method1_mons(seed, MUDKIP, 1000))
    mudkips.sort(key=method1_key)
    print('Mudkip')
    for i, pid, ivs in mudkips[:5]:
        print(f'{i+cycle:>5} {r_nature[pid % 25]} {pid:08x} {ivs}')
    print('Mudkip glitch')
    glitch_kips = filter(lambda t: corruptible(t[1], tid), mudkips)
    for j, pid, ivs in list(glitch_kips)[:5]:
        print(f'{j+cycle:>5} {r_nature[pid % 25]} {pid:08x} {ivs}')
    for i, base in enumerate(seeds(seed, limit=limit), 0):
        otId = ((base >> 16) << 16) | tid
        if otId & 0xff000000 == 0x04000000:
            continue
        print(f'{i+cycle:04d} ID: {otId:08x}')
        # print('Bootstrap (Wild-nodiff)')
        # triples = wild_mons(base, MUDKIP+15000, 60*60*60)
        # pairs = ((t[0], t[2]) for t in triples)
        # for total, i, pid, evs, address, pos in bootstrap_names(otId, pairs):
        #     if total < 50:
        #         box, index = divmod(pos, 30)
        #         print(f'{i+cycle:>6} {pid:08x} {total} {evs} {address:08x} Box {box+1} {index+1}')
        print('Bootstrap (Wild-pure)')
        triples = wild_mons(base, MUDKIP+15000, 60*60*60, diff=True)
        pairs = ((t[0], t[-1]) for t in triples)
        for total, i, pid, evs, address, pos in bootstrap_names(otId, pairs):
            if total < 50:
                box, index = divmod(pos, 30)
                print(f'{i+cycle:>6} {pid:08x} {total} {evs} {address:08x} Box {box+1} {index+1}')


def seek(seed, offset=0, limit=10, chance=0, acc_stage=6, evade=6, move_acc=95):
    chances = (16, 8, 4, 3, 2)
    dividends = (33, 36, 43, 50, 60, 75, 1, 133, 166, 2, 233, 133, 3)
    divisors = (100, 100, 100, 100, 100, 100, 1, 100, 100, 1, 100, 50, 1)
    assert len(divisors) == len(dividends) == 13
    buff = acc_stage + 6 - evade
    calc = dividends[buff] * move_acc
    calc //= divisors[buff]
    for base in seeds(seed, offset, limit=limit):
        value = base >> 16
        acc = (value % 100) + 1
        crit = (value % chances[chance]) == 0
        dmg = 100 - (value % 16)
        print(f'{base:08x}:{acc:03d}/{calc:03d}{str(acc <= calc)[0]}:{dmg:03d}{"!" if crit else ""}', end=' ')
    print()


def avoid(seed, limit=10, diff=False, bike=False, rate=20):  # Avoid wild encounters
    l = []
    offset = 2
    rate *= 16
    rate = (80 * rate // 100) if bike else rate
    rate = min(rate, 2880)
    for rng in seeds(seed, offset, limit):
        src = (r >> 16 for r in seeds(rng, limit=2))
        if diff and not next(src) % 100 < 60:
            is_enc = False
        elif not next(src) % 2880 < rate:
            is_enc = False
        else:
            is_enc = True
        calls = 2-len(list(src))
        l.append(f'{rng:08x}:{str(is_enc)[0]}:{calls}')
    print(' '.join(l))


def explore_moves(start, end=0xfffe):  # Explore offsets that glitch moves read
    with open('../pokeemerald/pokeemerald.gba', 'rb') as f:
        for move in range(start, end+1):
            offset = 0x082c8d6c + move * 4
            f.seek(offset & 0xffffff)
            value = int.from_bytes(f.read(4), 'little', signed=False)
            if value & 0xfff00000 == 0x02000000:
                print(f'{move:04x} {offset:08x} {value:08x}')


id_seed = 0x0936a1cd
cycle = 3009
tid = 0x8271
otId = ((id_seed >> 16) << 16) | tid
MUDKIP = 7095
good = [(0xfec71a4c, 0xa035, 3000)]


if __name__ == '__main__':
    pass
