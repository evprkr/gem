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
        self.tab_chars = 4

        self.exit = False # Set to true when the editor should close (at the end of the current update cycle)
        
        self.screen.bkgdset(' ', curses.color_pair(Colors.Background))

    # Cursor Position -> Buffer Position Translation
    def cursor_pos(self):
        return self.cursor.row - self.buffer.row_offset, self.buffer.margin_left + (self.cursor.col - self.buffer.col_offset)


    # Erase screen, redraw lines, redraw statusline, reposition cursor
    def refresh(self): # FIXME This is kind of a mess. Hard to read.
        self.screen.erase()

        # Draw empty line characters
        for i in range(self.buffer.rows):
            self.screen.addstr(i, 0, ' ~', curses.color_pair(Colors.LineNumbers))

        # Draw lines w/ line numbers
        for row, line in enumerate(self.buffer.lines[self.buffer.row_offset:self.buffer.row_offset + self.buffer.rows]):
            # Line Number
            line_nr = f"{row+self.buffer.row_offset+1}" # Offset single digit numbers
            if row+self.buffer.row_offset+1 < 10: line_nr = " " + line_nr
          
            if row == self.cursor.row - self.buffer.row_offset: self.screen.addstr(row, 0, f"{line_nr}", curses.color_pair(Colors.CursorLineNumber))
            else: self.screen.addstr(row, 0, f"{line_nr}", curses.color_pair(Colors.LineNumbers))

            # Line Text
            line_txt = line[self.buffer.col_offset:self.buffer.col_offset + self.buffer.cols - 2]
            self.screen.addstr(row, 3, f"{line_txt}", curses.color_pair(Colors.BufferText))

        # Update buffer's statusline
        self.buffer.statusline.update(self.screen, self.cursor)

        # Update debug window
        try:
            cursor_char = self.buffer.get_char(self.cursor)
            cursor_ascii = ord(cursor_char)
        except:
            cursor_char = 'NONE'
            cursor_ascii = 'N/A'

        if cursor_ascii == 10: cursor_char = 'NL'

        self.windows[0].body = [
            "* Buffer",
            f"  - line count: {self.buffer.line_count()}",
            f"  - col_offset: {self.buffer.col_offset}",
            f"  - row_offset: {self.buffer.row_offset}"
            "",
            f"* Line",
            f"  - Len: {len(self.buffer.get_line(self.cursor))}",
            f"  - Char: {cursor_char} ({cursor_ascii})",
        ]
        self.windows[0].update()

        # Print windows
        for w in self.windows:
            w.print(self.screen)

        # Reposition cursor
        self.screen.move(*self.cursor_pos())


    # Save buffer contents to file
    def save_buffer(self):
        contents = self.buffer.lines
#        for line in self.buffer.lines:
#            contents.append(line)

        f = open(self.buffer.filename, 'w')
        f.writelines(contents)
        f.close()
        self.buffer.dirty = False


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

        # Return to Normal Mode
        if key == chr(27):
            self.handle_esc_key(key)
            return

        # Normal Mode
        elif self.cursor.mode == "NORMAL":
            if key == Keys.CursorLeft or key == Keys.CursorRight or key == Keys.CursorUp or key == Keys.CursorDown: self.cursor.move(key)
            elif key == Keys.Exit: self.exit = True
            elif key == Keys.Save: self.save_buffer()
            elif key == Keys.Insert: self.cursor.mode = "INSERT"
            elif key in Keys.Delete:
                self.buffer.delete_char(self.cursor)
                self.buffer.dirty = True
            elif key in Keys.Backspace:
                self.buffer.backspace(self.cursor)
                self.buffer.dirty = True
            elif key == Keys.LineStart:
                self.cursor.goto(self.cursor.row, 0)
            elif key == Keys.LineEnd:
                self.cursor.col = len(self.buffer.get_line(self.cursor)) - 1;
                self.cursor.hint = self.cursor.col
                self.buffer.scroll(self.cursor)
            elif key == Keys.LineDelete:
                if self.buffer.line_count() > 1: self.buffer.lines.pop(self.cursor.row)
                else: self.buffer.lines[self.cursor.row] = '\n'
                self.cursor.col = 0
                self.cursor.hint = self.cursor.col
                self.buffer.scroll(self.cursor)
            elif key == Keys.Append:
                self.cursor.col = len(self.buffer.get_line(self.cursor)) - 1;
                self.cursor.hint = self.cursor.col
                self.buffer.scroll(self.cursor)
                self.cursor.mode = "INSERT"


        # Insert Mode
        elif self.cursor.mode == "INSERT":
            self.buffer.dirty = True
            if key == '\n':
                self.buffer.split_line(self.cursor)
                self.cursor.move(Keys.CursorDown)
            else:
                if key in Keys.Backspace:
                    self.buffer.backspace(self.cursor)
                elif key == Keys.Delete[0]:
                    self.buffer.delete_char(self.cursor)
                elif key == Keys.Tab:
                    for i in range(self.tab_chars):
                        self.buffer.insert_char(self.cursor, ' ')
                        self.cursor.move(Keys.CursorRight)
                else:
                    self.buffer.insert_char(self.cursor, key)
                    self.cursor.move(Keys.CursorRight)
