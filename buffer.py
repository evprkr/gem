# buffer.py

# Buffers are areas where text can be edited

from keys import *
from statusline import *
from color import *

class Buffer:
    def __init__(self, filename, lines, rows, cols):
        self.filename = filename # File loaded in buffer
        self.lines = lines # Buffer contents (text)
        self.dirty = False # If file has unsaved changes

        self.rows = rows # Total number of rows in the buffer
        self.cols = cols # Total number of cols in the buffer

        self.row_offset = 0 # Vertical offset for scrolling
        self.col_offset = 0 # Horizontal offset for scrolling
        self.scroll_offset_v = 5 # Row offset where vertical scrolling begins
        self.scroll_offset_h = 10 # Col offset where horizontal scrolling begins

        self.margin_top = 0 # Top cursor boundary offset
        self.margin_left = 3 # Left cursor boundary offset
        self.margin_right = 0 # Right cursor boundary offset
        self.margin_bottom = 0 # Bottom cursor boundary offset

        self.statusline = Statusline(self, self.rows, 0)
        self.prev_char = ''


    # Properties
    @property
    def bottom(self):
        return self.row_offset + self.rows - 1

    @property
    def right(self):
        return self.col_offset + self.cols - 3


    # Get total number of lines
    def line_count(self):
        return len(self.lines)


    # Get character under cursor
    def get_char(self, cursor):
        return self.lines[cursor.row][cursor.col]


    # Get line under cursor
    def get_line(self, cursor):
        return self.lines[cursor.row]


    # Get specific line from lines
    def get_line_idx(self, index):
        return self.lines[index]


    # Insert character at the cursor position
    def insert_char(self, cursor, char):
        cur_line = self.lines.pop(cursor.row)
        new_line = cur_line[:cursor.col] + char + cur_line[cursor.col:]
        self.lines.insert(cursor.row, new_line)


    # Split line at cursor position (moving second half of the split to the next line)
    def split_line(self, cursor):
        row, col = cursor.row, cursor.col
        cur_line = self.lines.pop(row)
        self.lines.insert(row, cur_line[:col]+'\n')
        self.lines.insert(row + 1, cur_line[col:])
        cursor.hint = 0 # Reset cursor to the beginning of the next line

    
    # Backspace character left of the cursor
    def backspace(self, cursor):
        row, col = cursor.row, cursor.col
        if col == 0:
            if row == 0: return

            cur_line = self.lines.pop(row)
            prev_line = self.lines.pop(row-1)
            new_line = prev_line[:-1] + cur_line
            self.lines.insert(row-1, new_line)

            cursor.row -= 1
            cursor.goto(row-1, len(prev_line)-1)
            self.scroll(cursor)
        else:
            cursor.move(Keys.CursorLeft)
            self.delete_char(cursor)


    # Delete character under the cursor
    def delete_char(self, cursor):
        row, col = cursor.row, cursor.col
        if (row, col) < (self.line_count()-1, len(self.lines[row])-1):
            if col < len(self.lines[row]) - 1:
                cur_line = self.lines.pop(row)
                new_line = cur_line[:col] + cur_line[col + 1:]
                self.lines.insert(row, new_line)
            else:
                cur_line = self.lines.pop(row)
                next_line = self.lines.pop(row)
                new_line = cur_line[:-1] + next_line
                self.lines.insert(row, new_line)


    # Vertical Scrolling
    def scroll(self, cursor):
        if cursor.row <= (self.row_offset + self.scroll_offset_v) - 1 and self.row_offset > 0:
            self.row_offset -= 1
        if cursor.row >= (self.bottom - self.scroll_offset_v) + 1 and self.bottom < len(self.lines) - 1:
            self.row_offset += 1
        if cursor.col == (self.col_offset + self.scroll_offset_h) - 1 and self.col_offset > 0:
            self.col_offset -= 1
        if cursor.col == (self.right - self.scroll_offset_h) + 1 and self.right < len(self.lines[cursor.row]) - 1:
            self.col_offset += 1

        # Scroll buffer to cursor when it goes offcreen
        while cursor.col > self.right:
            self.col_offset += 1;

        while cursor.col < self.col_offset:
            self.col_offset -= 1;
