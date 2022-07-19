from src.pylejandria.gui import load
from random import choice

def change(widget, property, values):
    widget[property] = choice(values)

functions = {
    'change': change
}

window = load('test.tk', functions)
window.mainloop()