import re
from pylejandria import gui
import tkinter as tk
from tkinter import ttk


def get_matches(text: str, expression: list[str]) -> list[str]:
    return [
        text[match.start():match.end()]
        for match in re.finditer(expression, text)
    ]


def replace(text: str, matches: list[str], replacement: str) -> str:
    index = 0
    for match in matches:
        current_text = text[index:]
        index += current_text.index(match)
        text = f'{text[:index]}{replacement}{text[index+len(match):]}'
        index += len(match)
    return text


def load_file() -> None:
    path = gui.ask('openfilename')
    if not path:
        return
    with open(path, 'r') as f:
        input_file.write(None, file=f, clear=True)


def check_file() -> None:
    text = input_file.read()
    matches = get_matches(text, '[\n]{3,}')
    text = replace(text, matches, 2*'\n')
    matches = get_matches(text, '[ \t]+\n')
    text = replace(text, matches, '\n')
    matches = get_matches(text, '\n\ndef')
    text = replace(text, matches, '\n\n\ndef')
    matches = get_matches(text, '\n\nclass')
    text = replace(text, matches, '\n\n\nclass')
    output_file.write(text, clear=True)


window = gui.Window('PEP8 Corrector', resizable=(False, False))

top_frame = tk.Frame(window)
upload_button = tk.Button(top_frame, text='Upload', command=load_file)
upload_button.grid(row=0, column=0, padx=10, pady=10)
check_button = tk.Button(top_frame, text='Check', command=check_file)
check_button.grid(row=0, column=1, padx=10, pady=10)
top_frame.pack(side='top', fill='x', padx=10, pady=10)

left_frame = ttk.LabelFrame(window, text='Input Code')
input_file = gui.TextArea(left_frame, width=80, height=40)
input_file.grid(row=0, column=0, sticky='ew')
left_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

right_frame = ttk.LabelFrame(window, text='Output Code')
output_file = gui.TextArea(right_frame, width=80, height=40)
output_file.grid(row=0, column=0, sticky='ew')
right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

window.mainloop()
