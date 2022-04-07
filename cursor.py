# cursor.py

class Cursor:
    def __init__(self, buffer, row, col):
        self.buffer = buffer # Which buffer cursor is in

        self.row = row # Cursor row position
        self.col = col # Cursor col position
        self.hint = 0 # Try to keep cursor col position between lines
 
    # Cursor Movement
    def move(self, key):
        if key == 'h': # Left
            if self.col > self.buffer.margin_left:
                self.col -= 1
                self.hint = self.col
        if key == 'l': # Right
            if self.col < len(self.buffer.lines[self.row]) - self.buffer.margin_right - 1:
                self.col += 1
                self.hint = self.col
        if key == 'k': # Up
            if self.row > self.buffer.margin_top:
                self.row -= 1
                self.col = min(self.hint, len(self.buffer.lines[self.row]) - 1)
        if key == 'j': # Down
            if self.row < len(self.buffer.lines) - self.buffer.margin_bottom - 1:
                self.row += 1
                self.col = min(self.hint, len(self.buffer.lines[self.row]) - 1)
        self.buffer.scroll(self)