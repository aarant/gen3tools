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


if __name__ == '__main__':
    with open('../pokeemerald/Emerald (J).gba', 'rb') as f:
        buffer = f.read()
        ace_targets(buffer, end=0x3110)
        #dump_words(buffer, 0x08283738, 4)
        #search(buffer, [0x02330000, 0x18020805, 0x82085727, 0x20000007])
