from src.pylejandria.gui import load
import sys
import tkinter as tk

sys.dont_write_bytecode = True


def change(widget, color1, color2):
    widget['bg'] = color1 if widget['bg'] == color2 else color2


def print_property(widget, property):
    print(widget[property])


if __name__ == '__main__':    
    window = load('c:/users/angel/python/pylejandria/test.tk', __file__)
    window.mainloop()