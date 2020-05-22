import os
import sys
import re
import random
from tqdm import tqdm
import subprocess

sys.path.append('/home/ariel/Desktop/Code/mgba/build/python/lib.linux-x86_64-3.7/')
from mgba import core, image

from pokemon import BoxMon

A = 1 << 0
B = 1 << 1
SELECT = 1 << 2
START = 1 << 3
RIGHT = 1 << 4
LEFT = 1 << 5
UP = 1 << 6
DOWN = 1 << 7
R = 1 << 8
L = 1 << 9


def run(core, n=1):
    for _ in range(n):
        core.run_frame()


def press(core, *keys, duration=1):
    core.set_keys(raw=sum(keys))
    run(core, duration)
    core.set_keys(raw=0)
    core.run_frame()


def read_mon(core, addr=0x020244ec):
    wram = core.memory.wram
    addr &= 0xffffff
    b = wram[addr:addr+80]
    assert(type(b) is bytearray)
    return b


def write_mon(core, mon, addr=0x020244ec):
    wram = core.memory.wram.u8
    addr &= 0xffffff
    for b, offset in zip(bytes(mon), range(addr, addr+80)):
        wram[offset] = b


def load_game(core, species=0x611):
    core.autoload_save()
    core.reset()
    run(core, 300)
    press(core, A)
    run(core, 50)
    press(core, A)
    run(core, 50)
    press(core, A)
    run(core, 100)
    press(core, A)
    run(core, 200)
    mon = BoxMon.from_buffer(read_mon(core))
    mon.decrypt()
    growth = mon.sub(0).type0
    if species != growth.species:
        growth.species = species
        mon.checksum = mon.calc_checksum()
        mon.encrypt()
        write_mon(core, mon)
        with open(f'fuzz/{species:04X}.pk3', 'wb') as f:
            f.write(bytes(mon))
    print(f'Species: {species:04X}')
    press(core, DOWN, duration=40)
    run(core, 30)
    press(core, A)
    run(core, 1000)
    save_png()


address_re = re.compile(r'Jumped to (\w+) address:? ([0-9a-fA-F]{7,8})\s*([^\r\n]*)')


def fuzz_species(d, species=0x611):
    global bar
    p = subprocess.run(['python3', 'harness.py', f'0x{species:0X}'], capture_output=True, encoding='utf-8')
    if p.stderr:
        with open(f'fuzz/stderr_{species:04X}.txt', 'w') as f:
            f.write(p.stderr)
    m = address_re.search(p.stdout)
    if m:
        kind, addr, extra = m.groups()
        if kind == 'EWRAM':
            s = f'{addr} {extra}'
        else:
            s = f'{addr}'
        bar.write(f'{species:04X} {s}')
        d[species] = s
    else:
        s = '?'
# 0817F114
# 0817F10C
# 03005E00 + E is tAnimId
# 0860EE10 sMonAnimFunctions?
# 0817F15C stores tAnimId
# returns to 0806EC9A
# tAnim in 03005E28+12=03005E34
# stored at 0806EDD4
# tAnimId = u8 at 0x0833155C+species-1

if __name__ == '__main__':
    if len(sys.argv) == 1:
        d = {}
        with open('fuzz/jumps.txt', 'r') as f:
            for line in f:
                species, value = line[:4], line[5:]
                species = int(species, 16)
                d[species] = value[:-1]
        l = list({species for species in range(0x611, 2**16) if species not in d})
        bar = tqdm(l)
        try:
            for species in bar:
                fuzz_species(d, species)
        except KeyboardInterrupt:
            bar.close()
            print('exited')
        with open('fuzz/jumps.txt', 'w') as f:
            for species, addr in sorted(d.items()):
                f.write(f'{species:04X} {addr}\n')
    else:
        species = int(sys.argv[1], 16)
        c = core.load_path('/home/ariel/Desktop/Code/pokeemerald/pokeemerald.gba')
        c = core.load_path('/home/ariel/Desktop/pokeemerald-fr.gba')
        i = image.Image(*c.desired_video_dimensions())
        c.set_video_buffer(i)
        def save_png(name=f'{species:04X}'):
            with open(f'fuzz/{name}.png', 'wb') as f:
                i.save_png(f)
        load_game(c, species)
