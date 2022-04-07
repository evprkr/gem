# editor.py

class Editor:
    def __init__(self, screen, buffer, cursor):
        self.screen = screen
        self.buffer = buffer
        self.cursor = cursor

    # Cursor Position -> Buffer Position Translation
    def cursor_pos(self):
        return self.cursor.row - self.buffer.row_offset, self.cursor.col - self.buffer.col_offset

    # Erase screen, redraw lines, reposition cursor
    def refresh(self):
        self.screen.erase()
        for row, line in enumerate(self.buffer.contents[self.buffer.row_offset:self.buffer.row_offset + self.buffer.rows]):
            self.screen.addstr(row, 0, line[self.buffer.col_offset:self.buffer.col_offset + self.buffer.cols])

        self.screen.move(*self.cursor_pos())

    # Handle Keypress
    def handle_keypress(self, key):
        match key:
            case ('h'|'j'|'k'|'l'):
                self.cursor.move(key)
            case _: pass
