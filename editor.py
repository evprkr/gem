# editor.py

class Editor:
    def __init__(self, buffer, width, height):
        self.buffer = buffer

        self.width = width # Terminal width in cols
        self.height = height # Terminal height in rows

        self.cursor_x = 0; # Cursor position (col)
        self.cursor_y = 0; # Cursor position (row)
        self.cursor_hint = 0; # Maintain cursor_x when changing lines

        self.offset_x = 0; # cursor_x minimum value offset
        self.offset_y = 0; # cursor_y minimum value offset

    def move_cursor(self, key):
        if key == 'h': # Left
            if self.cursor_x > self.offset_x:
                self.cursor_x -= 1
                self.cursor_hint = self.cursor_x
        if key == 'l': # Right
            if self.cursor_x < len(self.buffer[self.cursor_y]) - 1:
                self.cursor_x += 1
                self.cursor_hint = self.cursor_x
        if key == 'k': # Up
            if self.cursor_y > self.offset_y:
                self.cursor_y -= 1
                self.cursor_x = min(self.cursor_hint, len(self.buffer[self.cursor_y]) - 1)
        if key == 'j': # Down
            if self.cursor_y < len(self.buffer) - self.offset_y - 1:
                self.cursor_y += 1
                self.cursor_x = min(self.cursor_hint, len(self.buffer[self.cursor_y]) - 1)
