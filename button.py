import subprocess
import re
import os

hex_exp = re.compile(r'\s*0x.{8} (.{8}) (.{8}) (.{8}) (.{8})')


def hexport(path):
    subprocess.run(['arm-none-eabi-as', '-mcpu=arm7tdmi', '-o', 'temp.o', path], check=True)
    p = subprocess.run(['readelf', '-x', '.text', 'temp.o'], capture_output=True, check=True, encoding='utf-8')
    instrs = []
    for line in p.stdout.split('\n'):
        m = hex_exp.match(line)
        if m:
            for word in m.group(1, 2, 3, 4):
                if word != ' '*8:
                    instrs.append('0x' + word)
    os.remove('temp.o')
    return '{' + ','.join(instrs) + '}'


if __name__ == '__main__':
    with open('hex.txt', 'w') as f:
        f.write(hexport('hof.s'))
