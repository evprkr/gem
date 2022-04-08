# editor.py

from keys import Keys

class Editor:
    def __init__(self, screen, buffer, cursor):
        self.screen = screen
        self.buffer = buffer
        self.cursor = cursor

        self.exit = False

    # Cursor Position -> Buffer Position Translation
    def cursor_pos(self):
        return self.cursor.row - self.buffer.row_offset, self.cursor.col - self.buffer.col_offset

    # Erase screen, redraw lines, redraw statusline, reposition cursor
    def refresh(self):
        self.screen.erase()
        for row, line in enumerate(self.buffer.lines[self.buffer.row_offset:self.buffer.row_offset + self.buffer.rows]):
            self.screen.addstr(row, 0, line[self.buffer.col_offset:self.buffer.col_offset + self.buffer.cols])

        self.screen.addstr(self.buffer.rows, 0, self.buffer.statusline.update(self.cursor))

        self.screen.move(*self.cursor_pos())

    # Handle Escape Characters
    def handle_esc_key(self, key):
        self.screen.nodelay(True)
        n = self.screen.getch()
        if n == -1: 
            if self.cursor.mode == "INSERT": self.cursor.mode = "NORMAL"
        self.screen.nodelay(False)

    # Handle Keypress
    def handle_keypress(self, key):
        if key == 27: self.handle_esc_key(key)

        elif self.cursor.mode == "NORMAL":
            if key == Keys.CursorLeft or key == Keys.CursorRight or key == Keys.CursorUp or key == Keys.CursorDown: self.cursor.move(key)
            elif key == Keys.Exit: self.exit = True
            elif key == Keys.Insert: self.cursor.mode = "INSERT"

        elif self.cursor.mode == "INSERT":
            if chr(key) == '\n':
                self.buffer.split_line(self.cursor)
                self.cursor.move(Keys.CursorDown)
            else:
                self.buffer.insert_char(self.cursor, chr(key))
                self.cursor.move(Keys.CursorRight)
