import sys
atoms = set(range(0xA1, 0xF0))
atoms.add(0)
atoms -= {0xA0, 0xAF, 0xB7, 0xB9, 0xEF}

rshifts = set()
for rshift in range(0, 8, 2):
    for v in atoms:
        if v & ((2**rshift)-1):
            continue
        rshifts.add(v >> rshift)

lshifts = set()
for lshift in range(0, 24, 2):
    for v in atoms:
        lshifts.add(v << lshift)

positives = atoms | rshifts | lshifts
print(f'{len(positives)} positives')
negatives = {-n-1 for n in positives}
values = positives | negatives


def find_sums_to(n):
    for v1 in values:
        for v2 in values:
            if v1 + v2 == n:
                print(f'{v1:x} + {v2:x} == {n:x}')


def find_closest_to(n, threshold=16):
    best, best_diff = None, float('inf')
    for v in values:
        diff = abs(n - v)
        if diff < best_diff:
            best, best_diff = v, diff
    if best_diff < threshold:
        print(f'{best:x} close to {n:x} ({best_diff:x})')


if __name__ == '__main__':
    n = int(sys.argv[1], base=0)
    # for m in range(24+30):
    #     o = n - m * 80
    #     print(f'{m} {o:04x}')
    #     find_closest_to(o)
    find_sums_to(n)
    for check in range(2**16):
        c1 = (check + 0x3FBF) & 0xFFFF
        c2 = (check + 0xC0) & 0xFFFF
        c2 = (c2 - 0xC101) & 0xFFFF
        if c1 != c2:
            print(f'{check:x} {c1:x} vs {c2:x}')
