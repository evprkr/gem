# statusline.py

import curses
from color import *

class Statusline:
    def __init__(self, buffer, row, col):
        self.buffer = buffer # Which buffer this statusline belongs to
        self.row = row
        self.col = col

    def update(self, screen, cursor):
        # Get percentage of the way the cursor is from the top of the buffer to the bottom
        if cursor.row == self.buffer.line_count()-1: percent = "BOT"
        if cursor.row == 0: percent = "TOP"
        else: percent = str(100 * ((cursor.row+1) / (self.buffer.line_count()))).split('.')[0] + "%"

        # Get cursor position in parent buffer
        cursor_pos = f"{cursor.col+1}, {cursor.row+1}"

        # Print statusline background
        for i in range(self.buffer.cols):
            screen.addstr(self.row, self.col+i, ' ', curses.color_pair(Colors.StatuslineMain))

        # Print Cursor Mode
        match (cursor.mode):
            case "NORMAL": color = Colors.StatusNormalMode
            case "INSERT": color = Colors.StatusInsertMode
            case "SELECT": color = Colors.StatusSelectMode
            case "PROMPT": color = Colors.StatusPromptMode
        
        screen.addstr(self.row, self.col, f" {cursor.mode} ", curses.color_pair(color) | curses.A_BOLD)

        # Print Filename
        if self.buffer.dirty:
            filename = f" {self.buffer.filename} * "
            filename_pos = len(f" {cursor.mode} ")
        else:
            filename = f" {self.buffer.filename} "
            filename_pos = len(f" {cursor.mode} ")

        

        screen.addstr(self.row, filename_pos, filename, curses.color_pair(Colors.StatusFilename))

        # Print Cursor Position
        cursor_pos = f" {cursor.row+1}, {cursor.col+1} "
        screen.addstr(self.row, self.buffer.cols-len(cursor_pos), cursor_pos, curses.color_pair(color) + curses.A_BOLD)

        # Print Buffer Position
        buffer_pos = f" {percent} "
        screen.addstr(self.row, self.buffer.cols-(len(cursor_pos) + len(buffer_pos)), buffer_pos, curses.color_pair(Colors.StatusBufferPos))
