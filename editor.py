# editor.py

# The Editor is the parent of most other classes

import curses
from keys import Keys
from color import *

class Editor:
    def __init__(self, screen, buffer, cursor):
        self.screen = screen
        self.buffer = buffer
        self.cursor = cursor

        self.windows = [] # Keeps track of all open "windows" (popups)

        self.exit = False # Set to true when the editor should close (at the end of the current update cycle)


    # Cursor Position -> Buffer Position Translation
    def cursor_pos(self):
        return self.cursor.row - self.buffer.row_offset, self.cursor.col - self.buffer.col_offset + self.buffer.margin_left


    # Erase screen, redraw lines, redraw statusline, reposition cursor // FIXME very hard to read
    def refresh(self):
        self.screen.erase()

        # Draw lines w/ line numbers
        for row, line in enumerate(self.buffer.lines[self.buffer.row_offset:self.buffer.row_offset + self.buffer.rows]):
            line_nr = f"{row+self.buffer.row_offset+1}"
            if row+self.buffer.row_offset+1 < 10:
                line_nr = " " + line_nr

            line_txt = line[self.buffer.col_offset:self.buffer.col_offset + self.buffer.cols - 2]

            self.screen.addstr(row, 0, f"{line_nr}", curses.color_pair(HighlightGroups.LineNumbers))
            self.screen.addstr(row, 3, f"{line_txt}", curses.color_pair(HighlightGroups.BufferText))

        # Update buffer's statusline
        self.screen.addstr(self.buffer.rows, 0, self.buffer.statusline.update(self.cursor))

        # Update debug window
        try:
            cursor_char = self.buffer.get_char(self.cursor)
            cursor_ascii = ord(cursor_char)
        except:
            cursor_char = 'NONE'
            cursor_ascii = 'N/A'

        self.windows[0].body = [
            f"LINE LEN: {len(self.buffer.get_line(self.cursor))}",
            f"CHAR: {cursor_char} ({cursor_ascii})"
        ]
        self.windows[0].update()

        # Print windows
        for w in self.windows:
            w.print(self.screen)

        # Reposition cursor
        self.screen.move(*self.cursor_pos())


    # Handle Escape Characters // TODO look into curses.ascii.ctrl() for this
    def handle_esc_key(self, key):
        self.screen.nodelay(True)
        n = self.screen.getch()
        if n == -1: 
            if self.cursor.mode == "INSERT": self.cursor.mode = "NORMAL"
        self.screen.nodelay(False)


    # Handle Keypress
    def handle_keypress(self, key):
        self.buffer.prev_char = key

        if key == chr(27): self.handle_esc_key(key)

        elif self.cursor.mode == "NORMAL":
            if key == Keys.CursorLeft or key == Keys.CursorRight or key == Keys.CursorUp or key == Keys.CursorDown: self.cursor.move(key)
            elif key == Keys.Exit: self.exit = True
            elif key == Keys.Insert: self.cursor.mode = "INSERT"

        elif self.cursor.mode == "INSERT":
            if key == '\n':
                self.buffer.split_line(self.cursor)
                self.cursor.move(Keys.CursorDown)
            else:
                if key in Keys.Backspace:
                    self.cursor.move(Keys.CursorLeft)
                    self.buffer.delete_char(self.cursor)
                elif key in Keys.Delete:
                    self.buffer.delete_char(self.cursor)
                else:
                    self.buffer.insert_char(self.cursor, key)
                    self.cursor.move(Keys.CursorRight)
