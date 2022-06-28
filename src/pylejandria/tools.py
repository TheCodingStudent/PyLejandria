"""
the module tools is a collection of functions for variety of things, it
contains functions for printing or simplify repetitive things.
"""

from math import floor, ceil
from typing import Any, Optional


def CENTER(text: str, space: int) -> str:
    """
    secondary function for prettify, it centers the given text and splits the
    space evenly.
    params:
        text: string to be centered.
        space: quantity of white space to split.
    """
    padding = (space-len(text))/2
    return f'{" "*floor(padding)}{text}{" "*ceil(padding)}'


class PrettifyError(Exception):
    """
    Custom Exception for Prettify function.
    """
    pass


class PrettyDictError(Exception):
    """
    Custom Exception for Pretty_dict function.
    """
    pass


def prettify(
        values: list[list[Any]],
        separator: Optional[str]='|',
        padding: Optional[int]=0,
        headers: Optional[bool]=False,
        orientation: Optional[str]='center',
        _print: Optional[bool]=True
) -> str:
    """
    prettify receives as main argument a 2D matrix and returns a string
    to make easier the visualization of data in console, mostly is for
    school projects, if is something more complicated it would be easier
    to use tkinter.

    params:
        separator: string that separated columns.
        padding: integer of white space to fill each item.
        headers: boolean to indicate if horizontal bar of headings is needed.
        centered: boolean to indiceate if text must be centered.
    """
    separator = " "*padding + separator + " "*padding
    total_rows = len(values)
    total_cols = max([len(row) for row in values])
    string_values = [[str(col) for col in row] for row in values]
    all_values = [row + [""]*(total_cols - len(row)) for row in string_values]
    col_values = [[row[i] for row in all_values] for i in range(total_cols)]
    lengths = [(col, max([len(i) for i in col])) for col in col_values]
    if orientation == 'left':
        padded_values = [
            [row + " "*(length - len(row)) for row in col]
            for col, length in lengths
        ]
    elif orientation == 'right':
        padded_values = [
            [" "*(length - len(row)) + row for row in col]
            for col, length in lengths
        ]
    elif orientation == 'center':
        padded_values = [
            [CENTER(row, length) for row in col]
            for col, length in lengths
        ]
    else:
        raise PrettifyError(
            "invalid orientation. Expected right, left or center."
        )
    row_values = [[col[i] for col in padded_values] for i in range(total_rows)]
    joined_rows = [separator.join(row) for row in row_values]
    if headers:
        joined_rows.insert(1, '-'*len(joined_rows[0]))

    if _print:
        print('\n'.join(joined_rows))
    return '\n'.join(joined_rows)


def pretty_dict(
        dictionary: dict,
        indent: Optional[int]=0,
        tab: Optional[str]=' '*4,
        _print: Optional[bool]=True
) -> str:
    """
    pretty_dict is a function to print dictionaries with indentation, it may be
    helpful for print debugging or console programs.

    params:
        dictionary: a dict with the info we want to display.
        indent: is a parameter used for the function to print nested dicts.
        tab: is a string to separate levels of indentation, it can be any
        string.
    """
    if not isinstance(dictionary, dict):
        raise PrettyDictError("Argument must be dict type.")
    if not dictionary.items():
        return '{}\n'
    result = tab*indent + '{\n'
    for key, value in dictionary.items():
        result += tab*indent + f'{tab}{key}: '
        if not isinstance(value, dict):
            result += f'{value}\n'
        else:
            result += pretty_dict(value, indent=indent+1)
    if _print:
        result + tab*indent + '}\n'
    return result + tab*indent + '}\n'

if __name__ == '__main__':
    a = [
        ['Armando', 'Javier', 'Demian', 'Loretto', 'Susana', 'Laili'],
        [1, 2, 3],
        [4, 5, 6, 7],
        [8, 9]
    ]
    print(prettify(a))
