def read_metatiles(path):
    metatiles = []
    with open(path, 'rb') as f:
        i = 0
        while True:
            b = f.read(2)
            if not b:
                break
            n = int.from_bytes(b, 'little')
            n &= 0xff
            print(f'{i:04X}: {n:02X}')
            i += 1
            metatiles.append(n)
    return metatiles


if __name__ == '__main__':
    read_metatiles('../pokeruby/data/tilesets/primary/general/metatile_attributes.bin')
