# Ink Editor - cursor.py
# github.com/leftbones/ink

from logger import log

import curses


class Cursor:
    def __init__(self):
        self.window = None
        self.mode = "NORMAL"
        self.row = 0
        self.col = 0

        self.row_hint = 0 # unused?
        self.col_hint = 0
        self.win_hint = None

        self.sel_start_row = 0
        self.sel_start_col = 0

    @property
    def line(self): # Returns the line under the cursor
        return self.window.contents[self.row]

    @property
    def char(self): # Returns the character under the cursr
        return self.line[self.col]

    @property
    def next_char(self): # Returns the character to the right of the cursor, or the character under the cursor if at the end of the line
        if self.col < len(self.line): return self.line[self.col + 1]
        else: return self.char

    @property
    def prev_char(self): # Returns the character to the left of the cursor, or the character under the cursor if at the beginning of the line
        if self.col > 0: return self.line[self.col - 1]
        else: return self.char

    @property # Returns the col of the last character of the current line
    def line_end(self):
        return len(self.line) - 1

    # Set the cursor to the specified mode
    def set_mode(self, mode):
        self.mode = mode
        self.update_memory()

    # Start select mode
    def start_select_mode(self):
        self.sel_start_row, self.sel_start_col = self.window.translate_pos(self)
        self.mode = "SELECT"

    # Start line select mode
    def start_line_select_mode(self):
        self.goto(self.row, 0, "LINE SELECT")
        self.sel_start_row, self.sel_start_col = self.window.translate_pos(self)

    # Send cursor information to the current window for it to reference
    def update_memory(self):
        self.window.cursor_mode = self.mode
        self.window.cursor_row = self.row
        self.window.cursor_col = self.col

    # Move cursor to a window, restoring its position based on the window's cursor memory
    def goto_window(self, window):
        self.window = window
        self.goto(window.cursor_row, window.cursor_col)

    # Move cursor to position, clamps to window limits, set cursor to mode if specified
    def goto(self, row, col, mode=None):
        if mode: self.mode = mode

        if row < 0: row = 0 + self.window.upper_edge
        if col < 0: col = 0 + self.window_left_edge
        if row > self.window.line_count - 1: row = self.window.line_count - self.window.lower_edge
        if col > len(self.window.contents[row]) - 1: col = len(self.window.contents[row]) - self.window.right_edge

        self.row = row
        self.col = col
        self.col_hint = col
        self.window.scroll(self)
        self.update_memory()

    # Move cursor up one row
    def move_up(self, num=1):
        if self.row > 0:
            self.row -= 1
            self.col = min(self.col_hint, len(self.window.contents[self.row]) - 1)
            self.window.scroll(self)
            self.update_memory()

    # Move cursor down one row
    def move_down(self, num=1):
        if self.row < self.window.line_count - self.window.lower_edge:
            self.row += 1
            self.col = min(self.col_hint, len(self.line) - 1)
            self.window.scroll(self)
            self.update_memory()

    # Move cursor left one col
    def move_left(self, num=1):
        if self.col > 0:
            self.col -= 1
            self.col_hint = self.col
            self.window.scroll(self)
            self.update_memory()

    # Move cursor right one col
    def move_right(self, num=1):
        if self.col < len(self.line) - 1:
            self.col += 1
            self.col_hint = self.col
            self.window.scroll(self)
            self.update_memory()
