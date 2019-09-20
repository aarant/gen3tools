import subprocess
import re
import os
import sys

hex_exp = re.compile(r'\s*0x.{8} (.{8}) (.{8}) (.{8}) (.{8})')


def hexport(path):
    subprocess.run(['arm-none-eabi-as', '-mcpu=arm7tdmi', '-o', 'temp.o', path], check=True)
    p = subprocess.run(['readelf', '-x', '.text', 'temp.o'], capture_output=True, check=True, encoding='utf-8')
    instrs = []
    raw = []
    for line in p.stdout.split('\n'):
        m = hex_exp.match(line)
        if m:
            for word in m.group(1, 2, 3, 4):
                if word != ' '*8:
                    instrs.append('0x' + word[-2:] + word[-4:-2] + word[-6:-4] + word[:2])
                    raw.append(word)
    os.remove('temp.o')
    with open('ugh.txt', 'w') as f:
        f.write(''.join(raw))
    return '{' + ','.join(instrs) + '}'


if __name__ == '__main__':
    with open('hex.txt', 'w') as f:
        f.write(hexport(sys.argv[1]))
