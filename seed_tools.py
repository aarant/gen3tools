from pokemon import BoxMon, perms


def get_next(seed, n):  # Print the n next seeds
    s = [seed]
    for i in range(n):
        s.append(0xffffffff & s[-1] * 0x41c64e6d + 0x6073)
    print(' '.join('%08x' % seed for seed in s))


def get_prev(seed, n):  # Print the n previous seeds
    s = [seed]
    for i in range(n):
        s.append(0xffffffff & (s[-1] - 0x6073) * 0xeeb9eb65)
    print(' '.join('%08x' % seed for seed in s[::-1]))


def seed_at(frame):  # Finds seed at frame n using weird exponentiation
    m = 2**32
    a = 0x41c64e6d
    b = 0x6073
    res = (a-1)*m
    return (((pow(a, frame, res)-1)%res)//(a-1)*b)%m
    return ((a**frame-1)//(a-1)*b) % m  # ?


def seeds(seed=0, frame=None, limit=2**32):  # Generator yielding seeds
    if frame:
        seed = seed_at(frame)
    yield seed
    for _ in range(limit):
        seed = 0xffffffff & seed * 0x41c64e6d + 0x6073
        yield seed


def seed_frame(seed):
    for i, seed2 in enumerate(seeds()):
        if seed2 == seed:
            return i


def pids(frame=0, limit=2**16):  # Generator yielding PIDs
    for seed1, seed2 in zip(seeds(frame=frame, limit=limit), seeds(frame=frame+1, limit=limit)):
        pid = ((seed2 >> 16) << 16) | (seed1 >> 16)
        yield pid


def wild_pids(frame=0, limit=2**16):  # Generates wild PIDs, since the nature is picked strangely
    for seed in seeds(frame=frame, limit=limit):
        nature = (seed >> 16) % 25
        # Advance twice
        seed = 0xffffffff & (seed * 0x41c64e6d + 0x6073)
        seed2 = 0xffffffff & (seed * 0x41c64e6d + 0x6073)
        pid = ((seed2 >> 16) << 16) | (seed >> 16)
        while pid % 25 != nature:  # Advance twice again
            seed = 0xffffffff & (seed2 * 0x41c64e6d + 0x6073)
            seed2 = 0xffffffff & (seed * 0x41c64e6d + 0x6073)
            pid = ((seed2 >> 16) << 16) | (seed >> 16)
        yield pid


def wild_frame(pid, frame=0, limit=2**16):  # Finds the frame a wild pid will be generated
    for i, pid2 in enumerate(wild_pids(frame=frame, limit=limit)):
        if pid == pid2:
            return i+frame


def test_pid_pair(pid, otId):  # Test if the pair can corrupt a spinda into having glitch move 0x1608
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
        #box_mon.export()
        return True
    return False


def berry_master(item=153, frame=800, limit=2**16):  # Finds frames for collecting pomeg berries
    mod = item-153
    for i, seed in enumerate(seeds(frame=800, limit=limit)):
        if (seed >> 16) % 10 == mod:
            print('{:08x} at {}'.format(seed, i+frame))


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
                #print('Seed {},{} passed'.format(turn, dmg))
                streak += 1
                if streak > 2:
                    pass
                    #print('Seed {} is on streak {}'.format(seed, streak))
                seed1 = 0xffffffff & seed2 * 0x41c64e6d + 0x6073
            else:
                break
        if streak > 2:
            print('Streak of {} found at frame {}, second {} seed {:08x}'.format(streak, frame, round(frame/60, 1), seed))
        if streak > max_streak:
            max_streak = streak
        if streak > 4:
            streaks[frame] = streak
        seed = 0xffffffff & seed * 0x41c64e6d + 0x6073
    print('Done')
    print(streaks)


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


def spinda_spots(pid):  # Coordinates of spinda spots
    body1, body2, ear_r, ear_l = pid >> 24, pid >> 16, pid >> 8, pid
    spots = (body1 & 0xff, body2 & 0xff, ear_r & 0xff, ear_l & 0xff)
    coords = [(s & 0xf, s >> 4) for s in spots]
    print(coords)


def glitch_move(otId, frame=700, limit=4000):  # Find glitch move PIDs, only TID is needed
    for i, pid in enumerate(wild_pids(frame=frame, limit=limit)):
        sub1, sub2 = perms[pid % 24][1], perms[pid % 24][2]
        pid2 = pid | 0x40000000
        sub1_p, sub2_p = perms[pid2 % 24][1], perms[pid2 % 24][2]
        if sub1_p == sub2:  # If the new substruct 1 (A) is where substruct 2 (E) was
            if test_pid_pair(pid, otId):  # If the pair is safely corruptible
                yield i+frame, pid


def bootstrap(otId, num_args=None, priority=0x10, frame=800, limit=4000):  # Finds bootstrap pokemon
    found = []
    for i, pid in enumerate(wild_pids(frame=frame, limit=limit)):
        if perms[pid%24][2] != 0:
            continue
        mon = BoxMon()
        mon.personality = pid
        mon.otId = otId
        sub2 = mon.sub(2).type2
        sub2.hpEV = 3
        sub2.attackEV = 0x11
        sub2.defenseEV = 0
        sub2.speedEV = 3
        sub2.spAttackEV = 2
        sub2.spDefenseEV = priority
        mon.decrypt()
        if num_args is not None and sub2.cool != num_args:
            continue
        evs = tuple(getattr(sub2, name) for name in ('hpEV', 'attackEV', 'defenseEV',
                                                     'speedEV', 'spAttackEV', 'spDefenseEV'))
        if sum(evs) > 510:
            continue
        found.append((sum(evs), pid, i+frame, evs))
    found.sort()
    for ev_sum, pid, frame, evs in found:
        print('{:08x} at {} with {} {}'.format(pid, frame, ':'.join(str(e) for e in evs), ev_sum))
    return found


def ace(otId, code, frame=800, limit=4000, pos=0, display=True):  # Finds pokemon for ASM
    assert len(code) <= 3
    found = []
    for i, pid in enumerate(wild_pids(frame=frame, limit=limit)):
        mon = BoxMon()
        mon.personality, mon.otId = pid, otId
        if perms[pid % 24][2] == pos:  # E substruct is in the right position
            sub2 = mon.sub(2)
            for j in range(min(3, len(code))):
                sub2.raw[j] = code[j]
            mon.decrypt()
            # Sum up the EVs
            sub2 = sub2.type2
            names = ('hpEV', 'attackEV', 'defenseEV', 'speedEV', 'spAttackEV', 'spDefenseEV')
            evs = tuple(getattr(sub2, name) for name in names[:len(code)*2])
            if sum(evs) > 510:  # Impossible, cannot make a pokemon with more than 510 EVs
                continue
            found.append((sum(evs), (pid, i+frame, evs)))
    if display:
        for ev_sum, (pid, i, evs) in sorted(found):
            print('pid: {:08x} at {:05d} EVs: {} sum: {}'.format(pid, i, ':'.join('%03d' % ev for ev in evs), ev_sum))
    return sorted(found)


def ace_sequence(otId, code, limit=4000, pos=0):  # Splits up code sequence into slices with jumps
    groups = []
    n_groups = len(code)//2
    for i in range(n_groups):
        partial = []
        for j in range(2*i, 2*i+2):
            partial.append(code[j])
        if i == n_groups-1 and len(code) % 2 == 1:
            partial.append(code[-1])
        elif i != n_groups-1:
            partial.append(0xe026)
        groups.append(partial)
    for mon_code in groups:
        lowest = ace(otId, mon_code, limit=limit, pos=pos, display=False)[0]
        print(' '.join('%04x' % x for x in mon_code))
        ev_sum, (pid, i, evs) = lowest
        print('pid: {:08x} at {:05d} EVs: {} sum: {}'.format(pid, i, ':'.join('%03d' % ev for ev in evs), ev_sum))
    

# Help display
# Absolute lowest frame possible is around 650 ish
# Banette offset is 267 from target frame
# Oddish offset is 267 from target frame
get_next(0, 5)
otId = 0x0d59efe7
assert list(seeds(frame=800, limit=0))[0] == seed_at(800)
print('RNG is at address 03005D80')
print('RNG cycle count at 020249c0')
print('gRandomTurnNumber is at 02024330')
# while True:
#     pressed = int(input('Pressed at: '))
#     pid = int(input('Wild PID: '), base=16)
#     for i, wpid in enumerate(wild_pids(frame=pressed-600, limit=pressed+600)):
#         if wpid == pid:
#             print('Frame {}, diff {}'.format(i+pressed-600, i-600))
