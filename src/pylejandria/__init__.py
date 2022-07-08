#################################
#   MADE BY: ARMANDO CHAPARRO   #
#################################

import os

def history() -> None:
    path, file = os.getcwd(), 'doc/history.txt'
    with open(os.path.join(path, file), 'r', encoding='UTF-8') as f:
        print(f.read())