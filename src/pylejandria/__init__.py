#################################
#   MADE BY: ARMANDO CHAPARRO   #
#################################

import os
import pathlib

PATH = str(pathlib.Path(__file__).parent.resolve())
ROOT = '\\'.join(PATH.split('\\')[:-2])
with open(os.path.join(ROOT, 'doc/history.txt'), 'r', encoding='UTF-8') as f:
    HISTORY = f.read()

MAFER = """
It´s hard to forget
someone who gave you
so much to remember.
I´ll always love you, Mafer.
"""