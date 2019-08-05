from collections import namedtuple

from seed import battle_seeds, seeds

# Stat dividends and divisors
dividends = (33, 36, 43, 50, 60, 75, 1, 133, 166, 2, 233, 133, 3)
divisors = (100, 100, 100, 100, 100, 100, 1, 100, 100, 1, 100, 50, 1)
crit_mod = (16, 8, 4, 3, 2)

def test(seed, frame=0):
    for base in seeds(seed, frame):
        print('%08x' % base)
        yield base >> 16


def advance(rng, n=1):  # Advance the rng by a battle frame
    for _ in range(2*n):
        next(rng)


Move = namedtuple('Move', ('name', 'acc'), defaults=(100,))
Mon = namedtuple('Mon', ('name', 'crit', 'acc', 'evade'), defaults=(0, 6, 6))


def acc_check(rng, move_acc, acc_stage=6, ev_stage=6):
    buff = acc_stage + 6 - ev_stage
    calc = dividends[buff] * move_acc
    calc //= divisors[buff]
    check = (next(rng) % 100) + 1
    return not check > calc


def sim_turn(rng, mon1, mon2, move1, move2=None, skip1=0, skip2=0, in_frames=0, in_skip=0):
    hit1 = acc_check(rng, move1.acc, mon1.acc, mon2.evade)
    print('hit:', hit1)
    advance(rng, 4)  # first char already printed
    print('advance 4')
    msg = mon1.name + ' used' + move1.name + '!'
    advance(rng, len(msg)-1)
    print('advance', len(msg)-1)  # skip all but the first character
    advance(rng, skip1)  # skip any extra frames
    print('skipped:', skip1)
    advance(rng, 4)  # skip ahead to crit calculation
    print('skip 4')
    crit1 = (next(rng) % crit_mod[mon1.crit]) == 0
    print('crit:', crit1)
    advance(rng, 3)  # advance to damage calc
    print('advance 3')
    dmg1 = 100 - (next(rng) % 16)
    print('dmg:', dmg1)
    if move2:
        print('Move 2')
        advance(rng, in_frames)
        print('inframes')
        for _ in range(in_skip):
            next(rng)
        print('inskip')
        hit2 = acc_check(rng, move2.acc, mon2.acc, mon2.evade)
        print('hit:', hit2)
        advance(rng, 5)
        print('5')
        msg = mon2.name + ' used' + move2.name + '!'
        advance(rng, len(msg)-1)
        print(len(msg)-1)
        advance(rng, skip2)
        advance(rng, 4)  # advance to crit calc
        crit2 = (next(rng) % crit_mod[mon2.crit]) == 0
        print('crit:', crit2)
        advance(rng, 3)
        dmg2 = 100 - (next(rng) % 16)
        print('dmg:', dmg2)


mon1 = Mon('Foe TREECKO')
mon2 = Mon(' .UovT!s')
move1 = Move('POUND', 100)
move2 = Move('TACKLE', 95)
