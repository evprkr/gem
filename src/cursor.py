from logger import *

class Cursor:
    def __init__(self, window):
        self.window = window
        self.mode = "NORMAL"
        self.buffer = None
        self.prev_buffer = None
        self.row = 0
        self.col = 0
        self.hint = 0

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

    # Update buffer's cursor memory
    def update_memory(self):
        self.buffer.cursor_row = self.row
        self.buffer.cursor_col = self.col
        self.buffer.cursor_mode = self.mode

    # Move cursor to position
    def goto(self, row, col, mode=None):
        if mode: self.mode = mode

        if row < 0: row = 0
        if row > self.buffer.line_count - 1: row = self.buffer.line_count - 1

        if col < 0: col = 0
        if col > len(self.buffer.get_line(row)) - 1: col = len(self.buffer.get_line(row)) - 1

        self.row = row
        self.col = col
        self.hint = self.col
        self.buffer.scroll(self)
        self.update_memory()

    # Move cursor up
    def up(self):
        if self.row > 0:
            self.row -= 1
            self.col = min(self.hint, len(self.buffer.lines[self.row]) - 1)
            self.buffer.scroll(self)
            self.update_memory()

    # Move cursor down
    def down(self):
        if self.row < self.buffer.line_count - 1:
            self.row += 1
            self.col = min(self.hint, len(self.line) - 1)
            self.buffer.scroll(self)
            self.update_memory()

    # Move cursor left
    def left(self):
        if self.col > 0:
            self.col -= 1
            self.hint = self.col
            self.buffer.scroll(self)
            self.update_memory()

    # Move cursor right
    def right(self):
        if self.col < len(self.line) - 1:
            self.col += 1
            self.hint = self.col
            self.buffer.scroll(self)
            self.update_memory()
