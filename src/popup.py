import curses
from logger import *

class PopupWindow:
    def __init__(self, row, col, title, buffer, parent, anchor=None, print_border=True, print_title=True):
        self.row = row
        self.col = col
        self.title = title
        self.buffer = buffer
        self.parent = parent
        self.anchor = anchor
        self.print_border = print_border
        self.print_title = print_title

        if not self.buffer.line_numbers: self.buffer.margin_left = 0

        # Set Width + Height
        if not self.buffer.rows: self.rows = len(self.buffer.lines)
        elif self.print_border: self.rows = self.buffer.rows + 1
        else: self.rows = self.buffer.rows
        if not self.buffer.cols: self.cols = len(max(self.buffer.lines, key=len))
        elif self.print_border: self.cols = self.buffer.cols + 1
        else: self.cols = self.buffer.cols

        # Compensate for borders + status line
        #if self.buffer.border: self.rows += 1
        #if self.buffer.status_line: self.rows += 1

        # Set Anchor
        if self.anchor == "center":
            self.row -= self.rows // 2
            self.col -= self.cols // 2
        elif self.anchor == "bottom right":
            self.row -= self.rows
            self.col -= self.cols

        self.buffer.row_shift = self.row
        self.buffer.col_shift = self.col + 2

        # Window
        self.screen = self.parent.derwin(self.rows, self.cols, self.row, self.col)

        # Set buffer's window to self
        self.buffer.window = self

    def __repr__(self):
        return f"[Window: '{self.title}' at ({self.row}, {self.col}), contains buffer '{self.buffer.name}']"
