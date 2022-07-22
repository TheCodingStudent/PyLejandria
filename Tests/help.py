import importlib
import pkgutil
from pylejandria.gui import Hierarchy, Window
from tkinter import ttk

root = Window('Module Documentation', '300x800')
modules = {
    letter: []
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
}


def get_info(package: ...):
    pass

for _, name, ispkg in pkgutil.iter_modules():
    if ispkg is True and not name.startswith('_'):
        try:
            module = {
                name: [
                    f'{name}.{attrib}'
                    for attrib in dir(importlib.import_module(name))
                    if not attrib.startswith('_')
                ]
            }
            index = name[0].upper()
            modules[index].append(module)
        except ModuleNotFoundError:
            pass

style = ttk.Style()
style.theme_use('default')
style.configure(
    'Treeview',
    background='#181818',
    foreground='#808080',
    rowheight=25,
    fieldbackground='#181818'
)
style.map(
    'Treeview',
    background=[('selected', '#205078')],
    foreground=[('selected', 'white')]
)

hierarchy = Hierarchy(root, ..., 'Modulos')
hierarchy.pack(expand=True, fill='both')

root.mainloop()
