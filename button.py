import subprocess
import os
import sys


def hexport(path):  # Export assembly file as bytes
    subprocess.run(['arm-none-eabi-as', '-mcpu=arm7tdmi', '-o', 'temp.o', path], check=True)
    subprocess.run(['arm-none-eabi-ld', '-T', 'linker.ld', '-o', 'temp.elf', 'temp.o'], check=True)
    subprocess.run(['arm-none-eabi-objcopy', '-O', 'binary', '-j', '.text', 'temp.elf', 'input.bin'], check=True)
    with open('input.bin', 'rb') as f_in, open('input.txt', 'w') as f_out:  # TODO: Remove txt
        b = f_in.read()
        f_out.write(b.hex())
    os.remove('temp.elf')


if __name__ == '__main__':
    hexport(sys.argv[1])
