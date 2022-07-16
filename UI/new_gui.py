import tkinter as tk
from pylejandria import gui
from pylejandria.gui import Window, style


def validate_phone():
    phone.validate()
    print(phone.is_valid)


VSCODE_STYLE = {
    'Label1': {
        'bg': '#181818',
        'fg': '#808080'
    },
    'Label2': {
        'bg': '#323232',
        'fg': '#ffffff'
    },
    'PhoneEntry': {
        'init': {
            'extensions': True,
            'text': 'VSCODE Phone Entry',
            'button': 'Validate...',
            'command': validate_phone
        },
        'bg': 'red'
    },
    'BlackEntry': {
        'bg': 'black',
        'fg': 'white'
    },
    'BlueGreenEntry': {
        'bg': 'blue',
        'fg': '#00ff00'
    }
}

window = Window()

label1 = style(
    window, VSCODE_STYLE, name='Label', alias='Label1', text='VSCODE Label 1'
)
label1.pack()
label2 = style(
    window, VSCODE_STYLE, name='Label', alias='Label2', text='VSCODE Label 2'
)
label2.pack()
phone = style(window, VSCODE_STYLE, name='PhoneEntry', from_=gui)
phone.pack()
entry = tk.Entry(window)
black_entry = style(None, VSCODE_STYLE, alias='BlackEntry', widget=entry)
black_entry.pack()
blue_entry = style(window, VSCODE_STYLE, name='Entry', alias='BlueGreenEntry')
blue_entry.pack()


window.mainloop()
