"""
Compilation of widgets that take as a basis the widgets of tkinter, can add
functions to make simple interfaces in a very simple way without losing
flexibility or having new widgets.
"""

import io
from pylejandria.constants import FILETYPES, PHONE_EXTENSIONS
import re
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk
from tkinter import filedialog
from typing import Any, Callable


class Window(tk.Tk):
    def __init__(
        self, title: str | None=None, size: str | None=None,
        resizable: tuple[bool, bool] | None=None, **kwargs
    ):
        """
        Tkinter Tk wrapper, simplifies give name and size to the window, also
        manages the delete window protocol.
        Params:
            title: title of the window.
            size: size of the window in format "width"x"height".
            resizable: enable resize width and/or height of the window.
        """
        super().__init__(**kwargs)
        if title is not None:
            self.title(title)
        if size is not None:
            self.geometry(size)
        if resizable is not None:
            self.resizable(*resizable)
        self.wm_protocol('WM_DELETE_WINDOW', self.quit)

    def quit(self) -> None:
        """Destroys the window and quits python."""
        self.destroy()
        exit()
    
    def __setitem__(self, key: str, value: Any) -> None:
        if key == 'title':
            self.title(value)
        elif key == 'size':
            self.geometry(value)
        elif key == 'resizable':
            self.resizable(value)
        else:
            super().__setitem__(key, value)


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
        self.configs = {}

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
            prefix = self.configs.get('prefix', '')
            configs = self.configs.copy()
            if prefix:
                configs.pop('prefix')
            linenum = prefix + str(i).split(".")[0]
            self.create_text(5, y, anchor="nw", text=linenum, **configs)
            i = self.textwidget.index("%s+1line" % i)
    
    def __setitem__(self, key, value):
        if key == 'fg':
            self.configs['fill'] = value
            self.redraw()
        elif key in ('font', 'prefix', 'justify'):
            self.configs[key] = value
            self.redraw()
        else:
            super().__setitem__(key, value)


class TextArea(tk.Frame):
    def __init__(
        self, *args, linecounter: bool | None=True,
        scrollbar: bool | None=True, width: int | None=80,
        height: int | None=40, tab: str | None='    ', **kwargs
    ):
        """
        Advanced TextArea inspired from tkinter, it allows to display a line
        counter.
        """
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = CustomText(
            self, width=width, height=height, wrap=tk.NONE, undo=True
        )
        self.tab = tab
        font = tkfont.Font(font=self.text['font'])
        tab_size = font.measure(tab)
        self.text.config(tabs=tab_size)
        if scrollbar is True:
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
    
    def __setitem__(self, key, value):
        if key in ('bg', 'font'):
            self.text[key] = value
            if self.__dict__.get('linenumbers'):
                self.linenumbers[key] = value
            if key == 'font':
                font = tkfont.Font(font=self.text['font'])
                tab_size = font.measure(self.tab)
                self.text.config(tabs=tab_size)
        elif key == 'tab':
            self.tab = value
            font = tkfont.Font(font=self.text['font'])
            tab_size = font.measure(self.tab)
            self.text.config(tabs=tab_size)
        elif key.startswith('line') and self.__dict__.get('linenumbers'):
            self.linenumbers[key.replace('line', '')] = value
        elif key in ('prefix', ):
            self.linenumbers[key] = value
        else:
            self.text[key] = value
    
    def bind(self, event, func):
        self.text.bind(event, func)
    
    def search(self, *args, **kwargs):
        self.text.search(*args, **kwargs)

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
    
    def tag_add(self, *args, **kwargs):
        self.text.tag_add(*args, **kwargs)
    
    def tag_config(self, *args, **kwargs):
        self.text.tag_config(*args, **kwargs)
    
    def insert(self, *args, **kwargs):
        self.text.insert(*args, **kwargs)

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
        regex: str | None='\+[0-9]{1,3}[0-9]{10}',
        valid_fg: str | None='green', invalid_fg: str | None='red',
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
        super().__init__(master, **kwargs)

        self.extension = extensions
        self.pattern = kwargs.get('regex', regex)
        self.is_valid = False
        self.valid_fg = valid_fg
        self.invalid_fg = invalid_fg

        if text is not None:
            self.label = tk.Label(self, text=text)
            self.label.grid(row=0, column=0)
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
            self.button = tk.Button(self, text=button, command=command)
            self.button.grid(row=0, column=3)
    
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
            self.number_entry['fg'] = self.valid_fg
        else:
            self.number_entry['fg'] = self.invalid_fg
    
    def __setitem__(self, key, value):
        if key == 'text':
            if self.__dict__.get('text'):
                self.label['text'] = value
            else:
                self.label = tk.Label(self, text=value)
                self.label.grid(row=0, column=0)
        elif key == 'command':
            if self.__dict__.get('button'):
                self.button['command'] = value
        elif key == 'button':
            if self.__dict__.get('button'):
                self.button['text'] = value
            else:
                self.button = tk.Button(self, text=value)
                self.button.grid(row=0, column=3)
        elif key == 'regex':
            self.pattern = value
        elif key == 'valid_fg':
            self.valid_fg = value
        elif key == 'invalid_fg':
            self.invalid_fg = value
        else:
            super().__setitem__(key, value)


class TextSpan(tk.Frame):
    def __init__(self, master: tk.Widget):
        self.master = master
        self.counter = 0
    
    def load(self):
        for i, config in enumerate(self.values):
            if self.mode == 'row':
                if isinstance(self.type, str):
                    widget = getattr(tk, self.type)
                else:
                    widget = self.type
                all_config = self.__dict__.get('config', {}) | config
                widget = widget(self.master, **all_config)
                setattr(self, f'item{self.counter}', widget)
                widget.grid(row=i, column=self.column, sticky='nw')
            elif self.mode == 'column': ...
            else: ...
            self.counter += 1

    def __setitem__(self, key, value):
        setattr(self, key, value)
        if all([self.__dict__.get(k) for k in ('type', 'mode', 'values')]):
            self.load()


class WindowMenu(tk.Menu):
    def __init__(self, master: tk.Widget, menu_dict: dict, **kwargs):
        super().__init__(master, **kwargs)
        master.config(menu=self)
        for menu, options in menu_dict.items():
            new_menu = tk.Menu(self)
            for name, option in options.items():
                if name == 'separator':
                    new_menu.add_separator(**option)
                elif name in ('tearoff', ):
                    new_menu[name] = option
                else:
                    new_menu.add_command(label=name, **option)
            self.add_cascade(label=menu, menu=new_menu)


class Container(tk.Frame):
    """
    Container es un marco especial que ofrece capacidades
    para mostrar multiples marcos y almacenarlos, esto es
    utilizado para alamcenar las diferentes herramientas
    del programa, en Window se crea un Container y ahi se
    ponen los marcos de herramientas.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        ##### PROPIEDADES #####
        self.master = master                        # guardamos al widget padre
        self.frames = {}                            # aqui estaran los marcos de la aplicacion
        self.current = None                         # este sera el numero de la pagina actual 
        self.current_frame = None
        self.grid_rowconfigure(0, weight = 1)       # creamos una cuadricula con una sola fila
        self.grid_columnconfigure(0, weight = 1)    # y una sola columna
    
    ##### FUNCIONES #####
    def show_frame(self, name):                     # esta funcion mostrara el marco que se le indique
        self.hide_current()                         # ocultar el marco anterior
        self.current = name                         # actualizamos el numero del marco actual
        self.current_frame = self.frames[name]
        frame = self.frames[name]                   # obtenemos el marco que queremos
        frame.grid(row=0, column=0, sticky='nsew')  # colocamos el marco en el contenedor
        frame.tkraise()                             # mostramos el marco
    
    def hide_current(self):                         # con esta funcion ocultamos el marco que este mostrandose
        if self.current == None: return             # si no hay marco entonces salimos de la funcion
        self.frames[self.current].grid_forget()     # si hay entonces lo quitamos de la pantalla
        self.current = None                         # y guardamos que ya no hay marco mostrandose
    
    def add_frame(self, frame, name):
        self.frames[name] = frame


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
    Returns:
        widget: the given widget with all aplied properties.

    """
    if alias is None:
        alias = name
    all_config = config.get(alias) | kwargs
    if init_config := all_config.get('init', {}):
        all_config.pop('init')
    if widget is None:
        widget = getattr(from_, name)(master, **init_config)
    for key, value in all_config.items():
        if key.startswith('.'):
            func = getattr(widget, key[1:])
            func(value)
        else:
            widget[key] = value
    return widget
