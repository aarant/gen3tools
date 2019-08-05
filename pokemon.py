""" Class to represent and manipulate box pokemon. """
from ctypes import LittleEndianStructure, Union, c_uint8 as u8, c_uint16 as u16, c_uint32 as u32
# struct BoxPokemon
# {
#     u32 personality; 0-4
#     u32 otId; 4-8
#     u8 nickname[POKEMON_NAME_LENGTH]; 8-18
#     u8 language; 18
#     u8 isBadEgg:1; 19
#     u8 hasSpecies:1; 19
#     u8 isEgg:1; 19
#     u8 unused:5; 19
#     u8 otName[PLAYER_NAME_LENGTH]; 20-27
#     u8 markings; 27
#     u16 checksum; 28-30
#     u16 unknown; 30-32
#     union
#     {
#         u32 raw[12];
#         union PokemonSubstruct substructs[4];
#     } secure;
#
# struct PokemonSubstruct3
# {
#  /* 0x00 */ u8 pokerus;
#  /* 0x01 */ u8 metLocation;
#
#  /* 0x02 */ u16 metLevel:7;
#  /* 0x02 */ u16 metGame:4;
#  /* 0x03 */ u16 pokeball:4;
#  /* 0x03 */ u16 otGender:1;
#
#  /* 0x04 */ u32 hpIV:5;
#  /* 0x04 */ u32 attackIV:5;
#  /* 0x05 */ u32 defenseIV:5;
#  /* 0x05 */ u32 speedIV:5;
#  /* 0x05 */ u32 spAttackIV:5;
#  /* 0x06 */ u32 spDefenseIV:5;
#  /* 0x07 */ u32 isEgg:1;
#  /* 0x07 */ u32 altAbility:1;
#
#  /* 0x08 */ u32 coolRibbon:3;
#  /* 0x08 */ u32 beautyRibbon:3;
#  /* 0x08 */ u32 cuteRibbon:3;
#  /* 0x09 */ u32 smartRibbon:3;
#  /* 0x09 */ u32 toughRibbon:3;
#  /* 0x09 */ u32 championRibbon:1;
#  /* 0x0A */ u32 winningRibbon:1;
#  /* 0x0A */ u32 victoryRibbon:1;
#  /* 0x0A */ u32 artistRibbon:1;
#  /* 0x0A */ u32 effortRibbon:1;
#  /* 0x0A */ u32 giftRibbon1:1;
#  /* 0x0A */ u32 giftRibbon2:1;
#  /* 0x0A */ u32 giftRibbon3:1;
#  /* 0x0A */ u32 giftRibbon4:1;
#  /* 0x0B */ u32 giftRibbon5:1;
#  /* 0x0B */ u32 giftRibbon6:1;
#  /* 0x0B */ u32 giftRibbon7:1;
#  /* 0x0B */ u32 fatefulEncounter:4;
#  /* 0x0B */ u32 obedient:1;
# };


class Substruct0(LittleEndianStructure):  # Growth substructure
    _fields_ = [('species', u16), ('heldItem', u16), ('experience', u32), ('ppBonuses', u8), ('friendship', u8)]

    def __str__(self):
        return '\n'.join('{}: {}'.format(k, v) for k, v in self.dump().items())

    def dump(self):
        return {tup[0]: '%s' % getattr(self, tup[0]) for tup in self._fields_}


class Substruct1(LittleEndianStructure):  # Attacks substructure
    _fields_ = [('moves', u16 * 4), ('pp', u8*4)]

    def __str__(self):
        return '\n'.join('{}:{}'.format(move, pp) for move, pp in zip(self.moves, self.pp))

    def dump(self):
        d = {}
        for i in range(4):
            d['move%d' % i] = '%d' % self.moves[i]
            d['pp%d' % i] = '%d' % self.pp[i]
        return d


class Substruct2(LittleEndianStructure):  # EVs & Condition
    _fields_ = [('hpEV', u8), ('attackEV', u8), ('defenseEV', u8), ('speedEV', u8),
                ('spAttackEV', u8), ('spDefenseEV', u8), ('cool', u8), ('beauty', u8),
                ('cute', u8), ('smart', u8), ('tough', u8), ('sheen', u8)]

    def __str__(self):
        return '\n'.join('{}: {}'.format(k, v) for k, v in self.dump().items())

    def dump(self):
        return {tup[0]: '%d' % getattr(self, tup[0]) for tup in self._fields_}


class Substruct3(LittleEndianStructure):  # Miscellaneous
    _fields_ = [('pokerus', u8), ('metLocation', u8), ('metLevel', u16, 7), ('metGame', u16, 4), ('pokeBall', u16, 4),
                ('otGender', u16, 1), ('unk', u32, 30), ('isEgg', u32, 1), ('altAbility', u32, 1)]

    def __str__(self):
        return '\n'.join('{}: {}'.format(k, v) for k, v in self.dump().items())

    def dump(self):
        return {tup[0]: '%d' % getattr(self, tup[0]) for tup in self._fields_}


class SubstructUnion(Union):
    _fields_ = [('type0', Substruct0), ('type1', Substruct1),
                ('type2', Substruct2), ('type3', Substruct3), ('raw', u16*6)]


class SecureUnion(Union):
    _fields_ = [('raw', u32*12), ('substructs', SubstructUnion*4)]


class BoxMon(LittleEndianStructure):
    _fields_ = [('personality', u32), ('otId', u32), ('nickname', u8 * 10), ('language', u8),
                ('isBadEgg', u8, 1), ('hasSpecies', u8, 1), ('isEgg', u8, 1), ('unused', u8, 5),
                ('otName', u8 * 7), ('markings', u8), ('checksum', u16), ('unknown', u16), ('secure', SecureUnion)]

    def __str__(self):
        return '\n'.join('{}: {}'.format(k, v) for k, v in self.dump().items())

    def decrypt(self):
        for i in range(12):
            self.secure.raw[i] ^= self.otId
            self.secure.raw[i] ^= self.personality

    def encrypt(self):
        for i in range(12):
            self.secure.raw[i] ^= self.personality
            self.secure.raw[i] ^= self.otId

    def sub(self, i):  # Substruct helper
        return self.secure.substructs[perms[self.personality % 24][i]]

    def calc_checksum(self):
        checksum = 0
        for i in range(4):
            sub = self.sub(i)
            for j in range(6):
                checksum += sub.raw[j]
                checksum &= 0xffff
        return checksum

    def dump(self):
        d = {}
        for tup in self._fields_:
            name = tup[0]
            if name == 'nickname' or name == 'otName':
                d[name] = ''.join(r_names[e] if e in r_names else '`' for e in getattr(self, name))
            elif name in ('secure', 'unknown', 'unused'):
                pass
            else:
                d[name] = '%x' % getattr(self, name)
        return d

    def get_raw(self):
        return bytes(self).hex()

    def export(self):
        s = ''.join('%02X' % i for i in bytes(self))
        print('\n'.join([' '.join(
            s[i:i + 8][6:] + s[i:i + 8][4:6] + s[i:i + 8][2:4] + s[i:i + 8][:2] for i in range(j, j + 4 * 8, 8)) for j
                         in range(0, 20 * 8, 32)]))
        print()
        print(s)

    def test_legality(self):
        if self.checksum != self.calc_checksum():
            print('Illegal')
            self.isBadEgg = 1
            self.isEgg = 1
            self.sub(3).type3.isEgg = 1
        else:
            print('Legal')


# Maps personalities to substruct order lists l
# Substruct i appears in position l[i]
perms = {0: [0, 1, 2, 3], 1: [0, 1, 3, 2], 2: [0, 2, 1, 3], 3: [0, 3, 1, 2], 4: [0, 2, 3, 1], 5: [0, 3, 2, 1],
         6: [1, 0, 2, 3], 7: [1, 0, 3, 2], 8: [2, 0, 1, 3], 9: [3, 0, 1, 2], 10: [2, 0, 3, 1], 11: [3, 0, 2, 1],
         12: [1, 2, 0, 3], 13: [1, 3, 0, 2], 14: [2, 1, 0, 3], 15: [3, 1, 0, 2], 16: [2, 3, 0, 1], 17: [3, 2, 0, 1],
         18: [1, 2, 3, 0], 19: [1, 3, 2, 0], 20: [2, 1, 3, 0], 21: [3, 1, 2, 0], 22: [2, 3, 1, 0], 23: [3, 2, 1, 0]}

# maps in-game characters to bytes
name_map = {'A': 0xBB, 'B': 0xBC, 'C': 0xBD, 'D': 0xBE, 'E': 0xBF, 'F': 0xC0, 'G': 0xC1, 'H': 0xC2, 'I': 0xC3,
            'J': 0xC4, 'K': 0xC5, 'L': 0xC6, 'M': 0xC7, 'N': 0xC8, 'O': 0xC9, 'P': 0xCA, 'Q': 0xCB, 'R': 0xCC,
            'S': 0xCD, 'T': 0xCE, 'U': 0xCF, 'V': 0xD0, 'W': 0xD1, 'X': 0xD2, 'Y': 0xD3, 'Z': 0xD4, ' ': 0x00,
            '.': 0xAD, ',': 0xB8, 'a': 0xD5, 'b': 0xD6, 'c': 0xD7, 'd': 0xD8, 'e': 0xD9, 'f': 0xDA, 'g': 0xDB,
            'h': 0xDC, 'i': 0xDD, 'j': 0xDE, 'k': 0xDF, 'l': 0xE0, 'm': 0xE1, 'n': 0xE2, 'o': 0xe3, 'p': 0xe4,
            'q': 0xe5, 'r': 0xe6, 's': 0xe7, 't': 0xe8, 'u': 0xe9, 'v': 0xea, 'w': 0xeb, 'x': 0xec, 'y': 0xed,
            'z': 0xee, '0': 0xA1, '1': 0xA2, '2': 0xA3, '3': 0xA4, '4': 0xa5, '5': 0xa6, '6': 0xa7, '7': 0xa8,
            '8': 0xa9, '9': 0xaa, '!': 0xab, '?': 0xac, '♂': 0xb5, '♀': 0xb6, '/': 0xba, '-': 0xae,
            '…': 0xb0, '“': 0xb1, '”': 0xb2, '‘': 0xb3, '’': 0xb4}
r_names = {v: k for k, v in name_map.items()}


def analyze(data: bytearray):
    box_mon = BoxMon.from_buffer(data)
    box_mon.decrypt()
    box_mon.sub(0).type0.species = 412
    box_mon.checksum = box_mon.calc_checksum()

    print(box_mon)
    for i in range(4):
        print(getattr(box_mon.sub(i), 'type%s' % i))
    print('calculated: %x' % box_mon.calc_checksum())
    box_mon.test_legality()
    s = ''.join('%02X' % i for i in bytes(box_mon))
    print('\n'.join(
        [' '.join(s[i:i + 8][6:] + s[i:i + 8][4:6] + s[i:i + 8][2:4] + s[i:i + 8][:2] for i in range(j, j + 4 * 8, 8))
         for j in range(0, 20 * 8, 32)]))
    print()
    box_mon.encrypt()
    s = ''.join('%02X' % i for i in bytes(box_mon))
    print('\n'.join([' '.join(s[i:i+8][6:] + s[i:i+8][4:6] + s[i:i+8][2:4] + s[i:i+8][:2] for i in range(j, j+4*8, 8)) for j in range(0, 20*8, 32)]))
    print()
    print(s)
    print(perms[box_mon.personality % 24])


def analyze_loop():
    while True:
        hex_dump = input()
        data = bytearray.fromhex(hex_dump)
        analyze(data)


if __name__ == '__main__':
    analyze_loop()
