from os.path import join as joinp

from PyInstaller.__main__ import run

from __init__ import __version__


args = ['-y', '--clean', '-F', '--noupx', '-w',
        '--hidden-import', 'PyQt5.sip',
        '--hidden-import', 'PyQt5',
        '-n', f'Gen3Tools-{__version__}', 'gui.py']


run(args)
