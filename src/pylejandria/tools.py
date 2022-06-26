"""
the module tools is a collection of functions for variety of things, it contains
functions for printing or simplify repetitive things.
"""

from math import floor, ceil
from typing import List, Any, Optional

class PrettifyError(Exception): 
    """
    Custom Exception for Prettify function.
    """
    pass

def prettify(
        values: List[List[Any]], 
        separator: Optional[str]='|', 
        padding: Optional[int]=0, 
        headers: Optional[bool]=False, 
        orientation: Optional[str]='center'
    ) -> str:
    """
    prettify receives as main argument a 2D matrix and returns a string 
    to make easier the visualization of data in console, mostly is for
    school projects, if is something more complicated it would be easier
    to use tkinter.

    separator: string that separated columns
    padding: integer of white space to fill each item
    headers: boolean to indicate if horizontal bar of headings is needed
    centered: boolean to indiceate if text must be centered
    """
    separator = " "*padding + separator + " "*padding                                                                                                                   # add white space to the separator
    total_rows = len(values)                                                                                                                                            # get number of total rows
    total_cols = max([len(row) for row in values])                                                                                                                      # get number of total columns
    string_values = [[str(col) for col in row] for row in values]                                                                                                       # convert all values to string in table
    all_values = [row + [""]*(total_cols - len(row)) for row in string_values]                                                                                          # fill empty spaces of the table
    col_values = [[row[i] for row in all_values] for i in range(total_cols)]                                                                                            # rotate table to fill items
    lengths = [(col, max([len(i) for i in col])) for col in col_values]                                                                                                 # get max lengths of each column
    if orientation == 'right': padded_values = [[row + " "*(length - len(row)) for row in col] for col, length in lengths]                                              # add white space to the left
    elif orientation == 'left': padded_values = [[" "*(length - len(row)) + row for row in col] for col, length in lengths]                                             # add white space to the right                              
    elif orientation == 'center': padded_values = [[" "*floor((length-len(row))/2) + row + " "*ceil((length-len(row))/2) for row in col] for col, length in lengths]    # add white space to the center
    else: raise PrettifyError("invalid orientation. Expected right, left or center")                                                                                    # if invalid orientation raise error
    row_values = [[col[i] for col in padded_values] for i in range(total_rows)]                                                                                         # rotate table
    joined_rows = [separator.join(row) for row in row_values]                                                                                                           # join each column
    if headers: joined_rows.insert(1, '-'*len(joined_rows[0]))                                                                                                          # add header separator if needed
    return '\n'.join(joined_rows)                                                                                                                                       # join each row and return string separated by newline
        
if __name__ == '__main__':
    table = [
        ["Javier", "Demian", "Armando", "Susana", "Loretto"],
        [1, 2, 3],
        [4, 5, 6, 7 ,8],
        [9, 10]
    ]

    print(prettify(table, padding=1))