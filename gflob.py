""" Grep text references in GameFreak's shift-JIS C code. """
import os
import sys
from glob import iglob


def glob_func(name, path, exts=('.c', '.h')):
    if path[-1] == os.sep:
        path += '**'
    else:
        path += os.sep + '**'
    print(f'Searching for {name} in {path}')
    for path in iglob(path, recursive=True):
        if any(path.endswith(ext) for ext in exts):
            found = set()
            # Try multiple encodings
            for encoding in ('shift_jis_2004', 'shift_jis', 'utf-8'):
                with open(path, 'r', encoding=encoding) as f:
                    try:
                        for i, line in enumerate(f):
                            if name in line:
                                if line[-2:] == '\r\n':
                                    line = line[:-2]
                                elif line[-1:] == '\n':
                                    line = line[:-1]
                                if i not in found:
                                    print(f'{path}: {i+1}: {line}')
                                    found.add(i)
                    except Exception as e:
                        print(f'{encoding}: {e.__class__.__name__}: {e}', file=sys.stderr)
                        continue
                    else:
                        break


if __name__ == '__main__':
    glob_func(sys.argv[2], sys.argv[1])
