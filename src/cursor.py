from logger import *

class Cursor:
    def __init__(self):
        self.mode = "NORMAL"
        self.buffer = None
        self.row = 0
        self.col = 0
        self.hint = 0
        self.blink = False

    @property # Current line in active buffer
    def line(self):
        return self.buffer.get_line(self.row)

    @property # Current character under cursor
    def char(self):
        return self.line[self.col]

    @property # Character to the right of the cursor
    def next_char(self):
        if self.col < len(self.line): return self.line[self.col+1]
        else: return self.char

    @property # Character to the left of the cursor
    def prev_char(self):
        if self.col > 0: return self.line[self.col-1]
        else: return self.char

    @property # Ending col of current line
    def line_end(self):
        return len(self.buffer.get_line(self.row)) - 1

    # Move cursor up
    def up(self):
        if self.row > 0:
            self.row -= 1
            self.col = min(self.hint, len(self.buffer.lines[self.row]) - 1)
            self.buffer.scroll(self)

    # Move cursor down
    def down(self):
        if self.row < len(self.buffer.lines) - self.buffer.margin_bottom - 1: # TODO Make a method to get line count
            self.row += 1
            self.col = min(self.hint, len(self.buffer.lines[self.row]) - 1)
            self.buffer.scroll(self)

    # Move cursor left
    def left(self):
        if self.col > 0:
            self.col -= 1
            self.hint = self.col
            self.buffer.scroll(self)

    # Move cursor right
    def right(self):
        if self.col < len(self.buffer.lines[self.row]) - 1: # TODO Make a method to get line length
            self.col += 1
            self.hint = self.col
            self.buffer.scroll(self)

    # Move cursor to position
    def goto(self, row, col, mode=None):
        if mode: self.mode = mode
        self.row = row
        self.col = min(self.hint, self.line_end)
        self.buffer.scroll(self)
