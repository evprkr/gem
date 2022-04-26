# Simple persistent statusline that displays buffer information in the last row

import curses
from logger import *
from widget import Widget

class Statusline(Widget):
    def __init__(self, name, buffer, row, col):
        super().__init__(name, buffer, row, col)


    def update(self):
        screen = self.buffer.window.screen
        row = self.row - self.buffer.margin_bottom
        col = self.col + self.buffer.border
        buff_cols = self.buffer.window.cols - self.buffer.border + 1
        cursor_row = self.buffer.cursor_row
        cursor_col = self.buffer.cursor_col

        # Background
        for i in range(col, buff_cols - 1): screen.addch(row, i, ' ', curses.A_REVERSE)
        try: screen.addch(row, buff_cols - 1, ' ', curses.A_REVERSE)
        except: screen.insch(row, buff_cols - 1, ' ', curses.A_REVERSE)

        # Cursor Mode
        cursor_mode = f" {self.buffer.cursor_mode} "
        screen.addstr(row, col, cursor_mode, curses.A_REVERSE | curses.A_BOLD)

        # Buffer Filename
        if self.buffer.dirty: file_name = f"{self.buffer.name} *"
        else: file_name = f"{self.buffer.name}"
        screen.addstr(row, len(cursor_mode), file_name, curses.A_REVERSE)

        # Cursor Position
        cursor_pos = f"{cursor_row + 1}:{cursor_col + 1}"
        for i, c in enumerate(cursor_pos):
            col = (buff_cols - len(cursor_pos) + i) - 1
            screen.addch(row, col, c, curses.A_REVERSE | curses.A_BOLD)

        # Buffer Position
        if cursor_row == 0: buffer_pos = "TOP "
        elif cursor_row == self.buffer.line_count - 2: buffer_pos = "BOTTOM "
        else: buffer_pos = f"{int((float(cursor_row) / float(self.buffer.line_count - 1)) * 100)}% "
        screen.addstr(row, buff_cols - (len(cursor_pos) + len(buffer_pos) + 1), buffer_pos, curses.A_REVERSE)
