def search(buffer, pattern):
    matches = set()
    for i in range(len(buffer)):
        words = [int.from_bytes(buffer[j:j+4], 'little') for j in range(i, i+4*len(pattern), 4)]
        is_match = True
        for word, match in zip(words, pattern):
            if word != match:
                is_match = False
                break
        if is_match:
            print('match')
            matches.add(i)
    print(len(matches), matches)


def dump_words(buffer, offset, n):
    index = offset - 0x08283738 + 2635576
    for i in range(index, index+4*n, 4):
        num = int.from_bytes(buffer[i:i+4], 'little')
        print('%08x' % num)


def ace_targets(buffer, start=356, end=0xfefe):
    for move in range(start, end+1):
        offset = 0x08283738 + (move-0x3110)*4
        index = offset - 0x08283738 + 2635576
        num = int.from_bytes(buffer[index:index+4], 'little')
        print(f'{move:04x} {num:08x}')
        if num & 0xfff0000 in (0x2330000, 0x2320000):
            input()
        elif num & 0xff000000 == 0x08000000:
            index2 = num - 0x08283738 + 2635576
            script = buffer[index2]
            if script == 0x1f:
                num2 = int.from_bytes(buffer[index2+1:index2+5], 'little')
                if num2 & 0xfff0000 in (0x2330000, 0x2320000):
                    print(f'\t{script} {num2:08x}')
                    input()


def canonicalize(addr: int):  # Un-mirror an address
    if addr & 0xf0000000:  # Invalid
        return addr
    if 0x02000000 <= addr < 0x03000000:
        return addr & 0x0203ffff
    else:
        return addr
        raise NotImplementedError(f'Address {addr:08X} not implemented.')


def front_sprite_callback(f, species: int):  # Calculate sprite callback address for a species
    if not 0 <= species < 2**16:
        raise Exception(f'Species {species} out of bounds')
    # JPN
    tAnimId = read(f, 0x082FA374+species-1, 1)  # sMonFrontAnimIdsTable[species - 1]
    target = read(f, 0x085D34E8+4*tAnimId)  # sMonAnimFunctions[tAnimId]
    # US
    tAnimId = read(f, 0x083299ec+species-1, 1)
    target = read(f, 0x0860aa88+4*tAnimId)
    # FR
    # tAnimId = read(f, 0x0833155C+species-1, 1)
    # target = read(f, 0x0860EE10+4*tAnimId)

    # target = canonicalize(target)
    # print(f'{target:08X}')
    return target

def back_sprite_callback(f, species: int, nature: int):  # Calculate back sprite callback
    if not 0 <= species < 2**16:
        raise Exception(f'Species {species} out of bounds')
    nature %= 25
    # US values
    sSpeciesToBackAnimSet = 0x0860A8C8
    sBackAnimNatureModTable = 0x0860AD2F
    sBackAnimationIds = 0x0860ACE4
    sMonAnimFunctions = 0x0860aa88
    # # JP values
    # sSpeciesToBackAnimSet = 0x085D3328
    # sBackAnimNatureModTable = 0x085D378F
    # sBackAnimationIds = 0x085D3744
    # sMonAnimFunctions = 0x085D34E8
    backAnimSet = read(f, sSpeciesToBackAnimSet+species, 1)  # sSpeciesToBackAnimSet[species] - 1
    if backAnimSet != 0:
        backAnimSet -= 1
    animId = 0xff & (3 * backAnimSet + read(f, sBackAnimNatureModTable+nature, 1))  # 3 * backAnimSet + sBackAnimNatureModTable[nature]
    tAnimId = read(f, sBackAnimationIds+animId, 1)  # sBackAnimationIds[animId]
    target = read(f, sMonAnimFunctions+4*tAnimId, 4)  # sMonAnimFunctions[tAnimId]
    return target

def list_front_sprite_callbacks(f):
    low = 0x02000000
    high = 0x03000000
    print('Species Nat Addr EVS')
    l = []
    for species in range(2**16):
        target = front_sprite_callback(f, species)
        target2 = canonicalize(target)
        if (low <= target < high) and target != 0x02020000 and target != 0x02fe0600:
            hp = species & 0xff
            at = (species >> 8) & 0xff
            l.append((species, target, hp, at))
    l.sort(key=lambda tup: tup[0])
    for species, target, hp, at in l:
        print(f'{species:04x} = {target:08x} ({hp:03d} HP {at:03d} AT)')

def list_back_sprite_callbacks(f):
    low = 0x02000000
    high = 0x03000000
    print('Species Nat Addr EVS')
    for species in range(2**16):
        for nature in range(25):
            target = back_sprite_callback(f, species, nature)
            target2 = canonicalize(target)
            if (low <= target < high):# and target != 0x02020000:
                hp = species & 0xff
                at = (species // 8) & 0xff
                print(f'{species:04x} {nature:02d} = {target:08x} {target2:08x} ({hp:03d} HP {at:03d} AT)')


def find_anims():
    rom_path = '/home/ariel/Desktop/pokeemerald-fr.gba'
    bases = None
    with open(rom_path, 'rb') as rom:
        from collections import defaultdict
        locations = defaultdict(set)
        addr = 0
        while True:
            b = rom.read(4)
            if len(b) != 4:
                print(f'Broke at 0x{addr | 0x08000000:04X}')
                break
            v = int.from_bytes(b, 'little')
            # input(f'{v:08X}')
            locations[v].add(addr | 0x08000000)
            addr += 4
        with open('fuzz/jumps.txt', 'r') as f:
            for line in f:
                species, value = line[:4], line[5:]
                species, value = int(species, 16), int(value, 16)
                print(f'{species:04X} {value:08X}')
                if species == 0x0672:
                    continue
                s = set()
                for v in range(value-5, value+2):
                    for loc in locations[v]:
                        for i in range(-256*4, 256*4, 4):
                            s.add(loc+i)
                if bases is None:
                    bases = s
                    print(f'->{len(bases)}')
                else:
                    inter = bases & s
                    if len(inter) < len(bases):
                        print(f'->{len(inter)}')
                    bases = inter
                if len(bases) == 1:
                    loc = bases.pop()
                    print(f'Found?: {loc:08X}')
                    break


def read(f, addr: int, size: int = 4, signed: bool = False):
    f.seek(addr & 0xffffff)
    b = f.read(size)
    i = int.from_bytes(b, 'little', signed=signed)
    # if size == 4:
    #     print(f'{i:08X}')
    # elif size == 2:
    #     print(f'{i:04X}')
    # elif size == 1:
    #     print(f'{i:02X}')
    return i


if __name__ == '__main__':
    with open('../pokeemerald/pokeemerald.gba', 'rb') as f:
        list_front_sprite_callbacks(f)
