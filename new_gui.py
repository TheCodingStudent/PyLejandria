from src.pylejandria.gui import load
from random import choice
import sys

sys.dont_write_bytecode = True

def change(widget, property, values):
    widget[property] = choice(values)

if __name__ == '__main__':    
    window = load('test.tk', __file__)
    window.mainloop()