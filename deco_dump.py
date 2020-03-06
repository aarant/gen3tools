from luvdis.analyze import ROM


gDecorations = 0x083C2A44


def deco_desc(rom):
    l = []
    for i in range(256):
        addr = gDecorations+28*i+20
        target = rom.read(addr, 4)
        l.append(target)
        if target & 0xff000000 == 0x02000000:
            print(f'{i:02X}: {target:08X}')
    return l


def deco_names(rom):
    max_count = 0
    for i in range(256):
        addr = gDecorations+28*i+1
        count = b = 0
        while b != 0xff:
            b = rom.read(addr, 1)
            addr += 1
            count += 1
        if count > max_count:
            max_count = count
            print(f'{i:02X}: {count}')


if __name__ == '__main__':
    rom = ROM('../pokeruby-jp/baserom.gba')
    deco_desc(rom)
    deco_names(rom)
