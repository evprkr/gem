import curses
from logger import *

class PopupWindow:
    def __init__(self, row, col, title, buffer, parent, anchor=None):
        self.row = row
        self.col = col
        self.title = title
        self.buffer = buffer
        self.parent = parent
        self.anchor = anchor

        # Set Width + Height
        if not self.buffer.rows: self.rows = len(self.buffer.lines)
        else: self.rows = self.buffer.rows
        if not self.buffer.cols: self.cols = len(max(self.buffer.lines, key=len))
        else: self.cols = self.buffer.cols

        # Increase height if the buffer has a border or status line
        if self.buffer.border: self.rows += 1
        if self.buffer.statusline: self.rows += 1

        # Set Anchor
        if self.anchor == "center":
            self.row -= self.rows // 2
            self.col -= self.cols // 2
        elif self.anchor == "bottom left":
            self.row -= self.rows
        elif self.anchor == "bottom right":
            self.row -= self.rows
            self.col -= self.cols

        self.buffer.row_shift = self.row
        self.buffer.col_shift = self.col

        # Window
        self.screen = self.parent.derwin(self.rows, self.cols, self.row, self.col)

        # Set buffer's window to self
        self.buffer.window = self

    def __repr__(self):
        return f"[Window: '{self.title}' at ({self.row}, {self.col}), contains buffer '{self.buffer.name}']"
