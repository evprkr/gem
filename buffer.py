# buffer.py

# Buffers are areas where text can be edited

from statusline import *
from color import *

class Buffer:
    def __init__(self, lines, rows, cols):
        self.lines = lines # Buffer contents (text)

        self.rows = rows # Total number of rows in the buffer
        self.cols = cols # Total number of cols in the buffer

        self.row_offset = 0 # Vertical offset for scrolling
        self.col_offset = 0 # Horizontal offset for scrolling
        self.scroll_offset_v = 10 # Row offset where vertical scrolling begins
        self.scroll_offset_h = 5 # Col offset where horizontal scrolling begins

        self.margin_top = 0 # Top cursor boundary offset
        self.margin_left = 3 # Left cursor boundary offset
        self.margin_right = 0 # Right cursor boundary offset
        self.margin_bottom = 0 # Bottom cursor boundary offset

        self.statusline = Statusline(self)
        self.prev_char = ''


    # Properties
    @property
    def bottom(self):
        return self.row_offset + self.rows - 1

    @property
    def right(self):
        return self.col_offset + self.cols - 1


    # Get total number of lines
    def line_count(self):
        return len(self.lines)


    # Get character under cursor
    def get_char(self, cursor):
        return self.lines[cursor.row][cursor.col]


    # Get line under cursor
    def get_line(self, cursor):
        return self.lines[cursor.row]


    # Insert character at the cursor position
    def insert_char(self, cursor, char):
        cur_line = self.lines.pop(cursor.row)
        new_line = cur_line[:cursor.col] + char + cur_line[cursor.col:]
        self.lines.insert(cursor.row, new_line)


    # Split line at cursor position (moving second half of the split to the next line)
    def split_line(self, cursor):
        row, col = cursor.row, cursor.col
        cur_line = self.lines.pop(row)
        self.lines.insert(row, cur_line[:col])
        self.lines.insert(row + 1, cur_line[col:])
        cursor.hint = 0 # Reset cursor to the beginning of the next line


    # Delete character under the cursor
    def delete_char(self, cursor):
        row, col = cursor.row, cursor.col
        if (row, col) < (self.bottom, len(self.lines[row])):
            if col < len(self.lines[row]):
                cur_line = self.lines.pop(row)
                new_line = cur_line[:col] + cur_line[col + 1:]
                self.lines.insert(row, new_line)
            else:
                cur_line = self.lines.pop(row)
                next_line = self.lines.pop(row)
                new_line = cur_line + next_line
                self.lines.insert(row, new_line)


    # Get specific line from lines
    def get_line_idx(self, index):
        return self.lines[index]


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
        while cursor.col > self.cols + self.col_offset:
            self.col_offset += 1;

        while cursor.col < self.col_offset:
            self.col_offset -= 1;
