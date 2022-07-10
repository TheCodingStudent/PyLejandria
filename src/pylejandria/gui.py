"""
Compilation of widgets that take as a basis the widgets of tkinter, can add
functions to make simple interfaces in a very simple way without losing
flexibility or having new widgets.
"""

import io
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from typing import Any

FILETYPES = {
    'PDF': '*.pdf',
    'JPEG': '*jpg;*.jpeg;*.jpe;*.jfif',
    'PNG': '*png',
    'TIFF': '*.tiff;*.tif'
}


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
        clear: bool | None=False
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
        self.text.insert('end', text)

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

    def build(self, tree, branch='main'):
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
                            self.treeview.insert(row_name, 'end', item, text=item)
                        except tk.TclError:
                            print(row_name, item, type(item))
            else:
                self.treeview.insert(row_name, 'end', items, text=items)
            self.treeview.move(row_name, branch, 'end')
            self.index += 1


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
    result = [(type_, FILETYPES.get(type_)) for type_ in types]
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
    kwargs['filetypes'] = filetypes(*types)
    return func(**kwargs)
