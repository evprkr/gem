# cursor.py

from keys import Keys

class Cursor:
    def __init__(self, buffer, row, col):
        self.buffer = buffer # Which buffer the cursor is located in
        self.mode = "NORMAL"

        self.row = row # Cursor row position
        self.col = col # Cursor col position
        self.hint = 0 # Try to keep cursor col position between lines
 
    # Cursor Movement
    def move(self, key):
        if key == Keys.CursorLeft: # Left
            if self.col > 0:
                self.col -= 1
                self.hint = self.col
        if key == Keys.CursorRight: # Right
            if self.col < len(self.buffer.lines[self.row]) - self.buffer.margin_right:
                self.col += 1
                self.hint = self.col
        if key == Keys.CursorUp: # Up
            if self.row > self.buffer.margin_top:
                self.row -= 1
                self.col = min(self.hint, len(self.buffer.lines[self.row]) - 1)
        if key == Keys.CursorDown: # Down
            if self.row < len(self.buffer.lines) - self.buffer.margin_bottom - 1:
                self.row += 1
                self.col = min(self.hint, len(self.buffer.lines[self.row]) - 1)
        self.buffer.scroll(self)
