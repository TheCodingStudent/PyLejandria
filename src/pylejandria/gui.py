"""
Compilation of widgets that take as a basis the widgets of tkinter, can add
functions to make simple interfaces in a very simple way without losing
flexibility or having new widgets.
"""

import io
import pylejandria
from pylejandria.constants import FILETYPES, PHONE_EXTENSIONS
import re
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from typing import Any, Callable


class Window(tk.Tk):
    def __init__(
        self, name: str | None=None, size: str | None=None,
        resizable: tuple[bool, bool] | None=None
    ):
        """
        Tkinter Tk wrapper, simplifies give name and size to the window, also
        manages the delete window protocol.
        Params:
            name: name of the window.
            size: size of the window in format "width"x"height".
            resizable: enable resize width and/or height of the window.
        """
        super().__init__()
        if name is not None:
            self.title(name)
        if size is not None:
            self.geometry(size)
        if resizable is not None:
            self.resizable(*resizable)
        self.wm_protocol('WM_DELETE_WINDOW', self.quit)

    def quit(self) -> None:
        """Destroys the window and quits python."""
        self.destroy()
        exit()


class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        """
        Changes the behaviour of the tkinter.Text widget, it adds events
        detections to update the line numbers.
        """
        tk.Text.__init__(self, *args, **kwargs)
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args) -> Any:
        """
        Calls all the necessary events from Tcl to update the widget and return
        the given result.
        """
        cmd = (self._orig,) + args
        try:
            result = self.tk.call(cmd)
        except Exception:
            return None
        if any([
            args[0] in ("insert", "replace", "delete"),
            args[0:3] == ("mark", "set", "insert"),
            args[0:2] == ("xview", "moveto"),
            args[0:2] == ("xview", "scroll"),
            args[0:2] == ("yview", "moveto"),
            args[0:2] == ("yview", "scroll")
        ]):
            self.event_generate("<<Change>>", when="tail")
        return result


class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        """
        Canvas based widget to display the line numbers of a TextArea, works in
        couple with CustomText.
        """
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget: CustomText) -> None:
        """Updates the attached CustomText."""
        self.textwidget = text_widget

    def redraw(self, *args) -> None:
        """redraw line numbers."""
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)


class TextArea(tk.Frame):
    def __init__(self, *args, linecounter=True, width=80, height=40, **kwargs):
        """
        Advanced TextArea inspired from tkinter, it allows to display a line
        counter.
        """
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = CustomText(self, width=width, height=height)
        self.vsb = tk.Scrollbar(
            self, orient="vertical", command=self.text.yview
        )
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="right", fill="both", expand=True)

        if linecounter is True:
            self.linenumbers = TextLineNumbers(self, width=30)
            self.linenumbers.attach(self.text)
            self.linenumbers.pack(side="left", fill="y")
            self.text.bind("<<Change>>", self._on_change)
            self.text.bind("<Configure>", self._on_change)

    def _on_change(self, event: tk.Event) -> None:
        """Updates the line numbers."""
        self.linenumbers.redraw()

    def clear(
        self, start: str | None='1.0', end: str | None='end'
    ) -> None:
        """
        Clears the text.
        Params:
            start: index of start.
            end: index of end to clear.
        """
        self.text.delete(start, end)

    def write(
        self, text: str, file: io.TextIOWrapper | None=None,
        clear: bool | None=False, insert: str | None='end'
    ) -> None:
        """
        Writes the given text.
        Params:
            text: text to write.
            file: file to extract text from.
            clear: optional if clear all text.
        """
        if clear is True:
            self.clear()
        if file is not None:
            text = file.read()
        self.text.insert(insert, text)

    def read(
        self, start: str | None='1.0', end: str | None='end'
    ) -> str:
        return self.text.get(start, end)


class Hierarchy(tk.Frame):
    def __init__(self, master, tree, title='Tree', **kwargs):
        """
        Tkinter treeview wrapper for easier creation of hierarchies.
        """
        super().__init__(master, **kwargs)

        self.treeview = ttk.Treeview(self)
        self.treeview.pack(expand=True, fill='both')
        self.treeview.insert('', '-1', 'main', text=title)
        self.index = 0
        self.build(tree)

    def build(self, tree: list[Any], branch: str | None='main') -> None:
        """
        Creates the necessary structure of ttk.Treeview to make it a hierarchy.
        """
        for title, items in tree.items():
            row_name = f'item{self.index}'
            self.treeview.insert('', str(self.index), row_name, text=title)
            if isinstance(items, list | tuple):
                for item in items:
                    if isinstance(item, dict):
                        self.index += 1
                        self.build(item, row_name)
                    else:
                        try:
                            self.treeview.insert(
                                row_name, 'end', item, text=item
                            )
                        except tk.TclError:
                            print(row_name, item, type(item))
            else:
                self.treeview.insert(row_name, 'end', items, text=items)
            self.treeview.move(row_name, branch, 'end')
            self.index += 1


class PhoneEntry(tk.Frame):
    def __init__(
        self, master: tk.Widget,
        text: str | None=None, extensions: bool=True,
        button: str | None=None, command: Callable=lambda: None,
        **kwargs
    ):
        """
        Compound widget to make a phone entry, with extension if wanted.
        Params:
            master: parent widget.
            text: optional label at the beginning.
            extensions: optional if code extensions.
            button: optional button name.
            command: optional command for button.
        """
        super().__init__(master)

        self.extension = extensions
        self.pattern = kwargs.get('regex', '.*')
        self.is_valid = False

        if text is not None:
            tk.Label(
                self, text=text
            ).grid(row=0, column=0)
        if extensions is True:
            self.extension_combobox = ttk.Combobox(
                self, values=PHONE_EXTENSIONS, width=5, state='readonly'
            )
            self.extension_combobox.current(0)
            self.extension_combobox.grid(row=0, column=1)
        self.number_entry = tk.Entry(self)
        self.number_entry.grid(row=0, column=2)
        self.number_entry.bind('<Key>', self.update_config)
        if button is not None:
            tk.Button(self, text=button, command=command).grid(row=0, column=3)

    def get(self) -> None:
        if not self.extension:
            return self.number_entry.get()
        return self.extension_combobox.get() + self.number_entry.get()

    def update_config(self, event) -> None:
        full_number = self.get() + event.char
        self.number_entry['fg'] = 'black'
        self.is_valid = re.match(self.pattern, full_number) is not None

    def validate(self, *args) -> None:
        if self.is_valid is True:
            self.number_entry['fg'] = '#00ff00'
        else:
            self.number_entry['fg'] = '#ff0000'


def filetypes(
    *types: list[str],
    all_files: bool | None=True
) -> list[tuple[str, str]]:
    """
    returns a list with the corresponding file types, is useful for tkinter
    filedialog.
    Params:
        types: all the types to be returned.
        all_files: appends the all files extension *.*.
    """
    result = []
    for _type in types:
        type_format = ';'.join([f'*{ext}' for ext in FILETYPES.get(_type)])
        result.append((_type, type_format))

    if all_files is True:
        result.append(('All Files', '*.*'))
    return result


def ask(property: str, *types, **kwargs) -> str:
    """
    Function to wrap all tkinter.filedialog functions, also creates its
    respective window.
    Params:
        property: name of the function to be called.
    """
    func = getattr(filedialog, f'ask{property}')
    tk.Tk().withdraw()
    if types:
        kwargs['filetypes'] = filetypes(*types)
    return func(**kwargs)


def style(
    master: tk.Widget, config: dict, name: str | None=None,
    alias: str | None=None, from_: Any | None=tk,
    widget: Any | None=None, **kwargs
) -> tk.Widget | Any:
    """
    Function to apply style to widgets, it can be already existing widgets or
    it can be indicated which want to be created.
    Params:
        master: parent widget.
        config: dictionary with all the properties of the widgets, each element
                of the dictionary must be another dictionary with name equal
                to the name of the widget or an alias and then its properties.
        name:   name of the widget to create, if not given then widget argument
                must be provided.
        alias:  name is used to know which widget is wanted, but alias
                references the name of the attribute from the config argument.
        from_:  module where to import the widget.
        widget: if there is a widget already created it can be also styled, if
                provided then name, master and from_ are not needed.

    """
    if alias is None:
        alias = name
    all_config = config.get(alias) | kwargs
    if init_config := all_config.get('init', {}):
        all_config.pop('init')
    if widget is None:
        widget = getattr(from_, name)(master, **init_config)
    for key, value in all_config.items():
        widget[key] = value
    return widget

def get_chunk(a: str, b: str, lines: list[str]) -> tuple[list[str], list[str]]:
    if b is None:
        return [], lines
    start = lines.index(a)
    end = lines.index(b, start+1)
    return lines[end:], [line.strip() for line in lines[start:end]]

def load(filename: str, tab: str | None='    ') -> tk.Widget:
    """
    Loads a file with extension *.tk and builds all the widgets, the idea is
    to have a setup more or less like QML, a cascade of widgets, is meant to
    simple UI.
    Params:
        filename: path of the *.tk file.

    Returns:
        tk.Widget: the builded widget from the given file.
    """
    with open(filename, 'r') as f:
        lines = f.read().split('\n')
        widget_names = [line for line in lines if not ':' in line]

    widgets = []
    chunks = []

    for name in widget_names:
        try:
            widget = getattr(tk, name.strip())
        except AttributeError:
            widget = eval(name.strip())
        if name.count(tab) == 0:
            widget()
        widgets.append(widget)

    for a, b in pylejandria.tools.pair(widget_names + [None], 2):
        lines, chunk = get_chunk(a, b, lines)
        widget = {'widget': chunk.pop(0)}

        for item in chunk:
            key, value = item.split(': ', maxsplit=1)
            widget[key] = value
        chunks.append(widget)
    
    pylejandria.tools.pretty_list(chunks)

    # for i in range(len(widgets)-1):
    #     widget1, info1 = widgets[i],
