# buffer.py

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
        self.margin_left = 0 # Left cursor boundary offset
        self.margin_right = 0 # Right cursor boundary offset
        self.margin_bottom = 0 # Bottom cursor boundary offset

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

    # Get specific line from lines
    def get_line(self, index):
        return self.lines[index]

    # Vertical Scrolling
    def scroll(self, cursor):
        if cursor.row == (self.row_offset + self.scroll_offset_v) - 1 and self.row_offset > 0:
            self.row_offset -= 1
        if cursor.row == (self.bottom - self.scroll_offset_v) + 1 and self.bottom < len(self.lines) - 1:
            self.row_offset += 1
        if cursor.col == (self.col_offset + self.scroll_offset_h) - 1 and self.col_offset > 0:
            self.col_offset -= 1
        if cursor.col == (self.right - self.scroll_offset_h) + 1 and self.right < len(self.lines[cursor.row]) - 1:
            self.col_offset += 1

        while cursor.col > self.cols + self.col_offset:
            self.col_offset += 1;

        while cursor.col < self.col_offset:
            self.col_offset -= 1;
