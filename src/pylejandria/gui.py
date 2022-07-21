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
    def __init__(self, master):
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


def get_chunk(a: str, b: str, lines: list[str]) -> tuple[list[str], list[str]]:
    """
    Extract the lines between widgets based on the name.
    Params:
        a: first widget.
        b: second widget.
        lines: lines of the source file.
    Returns:
        the remaining lines to not repeat and the stripped lines between
        widgets, also the indent level.
    """
    if b is None:
        return [], [line.strip() for line in lines], a.count('    ')
    start = lines.index(a)
    end = lines.index(b, start+1)
    return (
        lines[end:], [line.strip() for line in lines[start:end]],
        a.count('    ')
    )


def find_attribute(name: str, sources: list[Any]) -> Any:
    """
    Returns the attribute from the given sources.
    Params:
        name: name of the attribute to return.
        sources: list of sources to search from.
    Returns:
        Any: the wanted attribute in case it exists. Else raises an error.
    """
    for source in sources:
        try:
            return getattr(source, name)
        except AttributeError:
            continue
    raise AttributeError(f'Attribute {name!s} not found')


def widget_info(chunk: list[str], indent: int) -> dict:
    """
    Gets a list of lines of a widget and returns a dictionary with its
    properties.
    Params:
        chunk: list of strings of a widget.
    Returns:
        widget: dict with all the properties extracted from the chunk.
    """
    widget = {}
    widget['widget'] = chunk.pop(0)
    widget['indent'] = indent

    for item in chunk:
        key, value = item.split(': ', maxsplit=1)
        if key in ('execute', ):
            if widget.get(key):
                widget[key].append(value)
            else:
                widget[key] = [value]
        else:
            try:
                widget[key] = eval(value)
            except:
                widget[key] = value
    return widget


def get_widgets(
    lines: list[str], names: list[str]
) -> list[dict | None, str | None]:
    """
    Evaluate the lines from the source file, checks between each of them, gets
    a chunk and then its info.
    Params:
        lines: lines from the source file.
        names: names of the widgets.
    Returns:
        widgets: a list with tuples containing a dictionary with the widget
        properties and its id in case it haves.
    """
    widgets = []
    for a, b in pylejandria.tools.pair(names + [None], 2):
        lines, chunk, indent = get_chunk(a, b, lines)
        widget = widget_info(chunk, indent)
        widgets.append((widget, widget.get('id')))
    widgets.append((None, None))
    return widgets


def place_widget(widget: Any, info: dict) -> None:
    """
    Manages the place method of the widget based on its info.
    Params:
        widget: widget to place.
        info: info of the widget.
    Returns:
        None
    """
    if info.get('.pack'):
        widget.pack(**info.pop('.pack'))
    elif info.get('.place'):
        widget.place(**info.pop('.place'))
    elif info.get('.grid'):
        widget.grid(**info.pop('.grid'))
    else:
        try:
            widget.pack()
        except AttributeError:
            pass

def widget_args(info: dict):
    """
    Extracts main arguments from the info of widget.
    Params:
        info: dictionary of properties of a widget.
    """
    args = []
    if info.get('parent'):
        args.append(info.pop('parent'))
    return args


def get_widget(widgets: dict, widget_id: str) -> Any:
    """
    Returns a widget based on its id, if it doesnt exists then raises an error.
    Params:
        widgets: dictionary of widgets with id as key.
        widget_id: id of the widget to return.
    Returns:
        widget: widget from the widgets dictionary.
    Raises:
        An AttributeError with a message to easily find which widget was not
        founded.
    """
    if widget := widgets.get(widget_id):
        return widget
    raise AttributeError(f'widget {widget_id!s} not found')


def get_variables(expression: str) -> list[str, list]:
    """
    Checks if the expression follows the following format, if so then returns
    the parsed expression and the arguments. The arguments are not evaluated.
    Format:
        - (arg1 | arg2 | ...)
    Params:
        expression: string expression to parse.
    Returns:
        expression: parsed expression.
        str_args: arguments from the expression.
    """
    if args := re.search('\(.*\)', expression):
        args = args.group()
        expression = expression.replace(args, '')
    str_args = [] if args is None else args[1:-1].split(' | ')
    return expression, str_args


def get_property(expression: str, widget: tk.Widget, widgets: dict) -> Any:
    """
    checks if the expression follows the following format, if so then returns
    the parsed expression and the proper value.
    Format:
        - self: refers to the widget itself.
        - #name: refers to a widget with id name.
        - [property]: returns the given property of the widget.
    Examples:
        - self.master
        - #topleft_frame.label['text']
    Params:
        expression: string expression to parse.
        widget: current widget, in case its referenced.
        widgets: dict of widgets, in case any is referenced.
    Returns:
        any: the corresponding value based on the expression.
    """
    property_ = None
    if args := re.search("\['.+'\]", expression):
        args = args.group()
        expression = expression.replace(args, '')
        property_ = eval(args[1:-1])
    if expression.startswith('#'):
        expression = expression.replace('#', '')
        widget_property = widgets.get(expression)
        if property_ is None:
            return widget_property
        return widget_property[property_]
    elif expression.startswith('self'):
        return widget[property_]
    else:
        widget_property = getattr(widget, expression)
        return widget_property[property_]


def parse_property(
    expression: str, widget: tk.Widget, widgets: dict, module: Any
) -> Any:
    """
    Checks if the expression follows the following format, if so then returns
    the corresponding property.
    Format:
        - $function_name: single function.
        - $function_name(arg1 | arg2 | ...): function with parameters.
        - self | #id: reference to itself or a widget with id.
        - (self | #id).property: refers to a property of the first item.
    Params:
        expression: string expression to parse.
        widget: current widget, in case its referenced.
        widgets: dict of widgets, in case any is referenced.
        module: loaded source file to be referenced.
    Returns:
        Any: the corresponding value.
    """
    if str(expression).startswith('$'):
        expression = expression.replace('$', '')
        args = []
        if str_args := re.search("\(.*\)", expression):
            expression, str_args = get_variables(expression)
            args = [
                parse_property(arg, widget, widgets, module)
                for arg in str_args
            ]
        func = getattr(module, expression)
        return lambda *e: func(*args)
    elif re.match("(self|#.+)(\.[a-z]*)*(\['[a-z]*'\]){0,1}", str(expression)):
        result = None
        for method in expression.split('.'):
            if method == 'self':
                result = widget
            elif method.startswith('#') or re.search("\['.+'\]", method):
                result = get_property(method, widget, widgets)
                return result if result else method
            else:
                if str_args := re.search("\(.*\)", method):
                    method, str_args = get_variables(method)
                    args = [
                        parse_property(arg, widget, widgets, module)
                        for arg in str_args
                    ]
                    func = getattr(result, method)
                    return lambda *e: func(*args)
                result = getattr(result, method)
        return result
    elif str_args := re.match("\(.*\)", str(expression)):
        expression, str_args = get_variables(expression)
        return [
            parse_property(arg, widget, widgets, module) for arg in str_args
        ]
    try:
        return eval(expression)
    except:
        return expression


def assign_parent(widget: Any, info1: dict, info2: dict) -> tk.Widget | None:
    """
    Assigns parent to the widget based on the indentation.
    Params:
        widget: current widget, is used to get the parent or be the parent.
        info1: dictionary of the current widget.
        info2: dictionary of the next widget.
    Returns:
        parent: parent widget of the current widget.
        Or None.
    """
    parent = widget
    indent1 = info1.get('indent')
    indent2 = info2.get('indent') if info2 else None
    if indent2 is None:
        return None
    if indent1 == indent2:
        parent = parent.master
    elif indent1 > indent2:
        for _ in range(indent1 - indent2 + 1):
            parent = parent.master
    return parent


def load(
    filename: str, file: str, parent: tk.Widget | None=None,
    style_dict: dict | None=None
) -> tk.Widget:
    """
    Loads a file with extension *.tk and builds all the widgets, the idea is
    to have a setup more or less like QML, a cascade of widgets, is meant to
    simple UI.
    Params:
        filename: path of the *.tk file.
        file: path of the source, to load functions and classes.
        parent: optional parent, in case the loaded widget is not a window.
        style_dict: optional dictionary with style based on alias.
    Returns:
        tk.Widget: the builded widget from the given file.
    """
    with open(filename, 'r') as f:
        lines = f.read().split('\n')
        widget_names = [line for line in lines if ':' not in line]

    module = pylejandria.tools.get_module(file) if file is not None else None
    widgets = get_widgets(lines, widget_names)
    window = None
    built = {}

    for info1, info2 in pylejandria.tools.pair(widgets, 2, index=0):
        if parent is not None:
            info1['parent'] = parent
            parent = None
        widget = find_attribute(
            info1.pop('widget'), (module, tk, tk.ttk, pylejandria.gui)
        )
        widget_arguments = widget_args(info1)
        widget = widget(*widget_arguments)
        if alias := info1.get('alias'):
            widget = style(None, style_dict, alias=alias, widget=widget)
        if id_ := info1.get('id'):
            built[id_] = widget
        if window is None:
            window = widget
        place_widget(widget, info1)

        for key, value in info1.items():
            if key in ('indent', 'id', 'alias'):
                continue
            elif key == 'execute':
                for func_value in value: 
                    if func := parse_property(func_value, widget, built, module):
                        func()
                continue
            property_ = parse_property(value, widget, built, module)
            if key.startswith('.'):
                func = getattr(widget, key.replace('.', ''))
                if isinstance(property_, (list, tuple)):
                    func(*property_)
                else:
                    func(property_)
            else:
                try:
                    widget[key] = getattr(module, str(property_))
                except AttributeError:
                    try:
                        widget[key] = property_
                    except tk.TclError:
                        print(f'invalid {key!a} property')

        if parent := assign_parent(widget, info1, info2):
            info2['parent'] = parent

    return window
