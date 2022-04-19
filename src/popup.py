from logger import *

class PopupWindow:
    def __init__(self, row, col, title, buffer, parent, anchor=None, print_border=True, print_title=True):
        self.row = row
        self.col = col
        self.title = title
        self.buffer = buffer
        self.parent = parent
        self.anchor = anchor
        self.print_border = print_border
        self.print_title = print_title


        # Append Newline Characters
        lines_copy = []
        for line in self.buffer.lines:
            if len(line) == 0 or line[-1] != '\n':
                lines_copy.append(line + '\n')
            else:
                lines_copy.append(line)

        self.buffer.lines = lines_copy.copy()

        # Row/Col Shifting
        if self.print_border:
            self.row_shift = 0
            self.col_shift = 0
        else:
            self.row_shift = 0
            self.col_shift = 0

        self.buffer.row_shift = self.row
        self.buffer.col_shift = self.col

        if not self.buffer.line_numbers: self.buffer.margin_left = 0

        # Set Width + Height
        if not self.buffer.rows: self.rows = len(self.buffer.lines)
        else: self.rows = self.buffer.rows + 1
        if not self.buffer.cols: self.cols = len(max(self.buffer.lines, key=len))
        else: self.cols = self.buffer.cols + 1

        # Set Anchor
        if self.anchor == "center":
            self.row = self.row - (self.rows // 2)
            self.col = self.col - (self.cols // 2)
        elif self.anchor == "bottom right":
            self.row = self.row - self.rows
            self.col = self.col - self.cols

        # Window
        self.screen = self.parent.derwin(self.rows + 1, self.cols, self.row, self.col)

        # Set buffer's window to self
        self.buffer.window = self

    def __repr__(self):
        return f"[Window: '{self.title}' at ({self.row}, {self.col}), contains buffer '{self.buffer.name}']"

    def update(self):
        # Background
        for r in range(0, self.buffer.rows + self.row_shift):
            for c in range(0, self.buffer.cols + 1):
                self.screen.insch(r, c, ' ')

        # Contents
        for row, line in enumerate(self.buffer.lines):
            try: self.screen.addstr(row + self.row_shift, self.col, line)
            except Exception as e: log.write(f"Window: Failed to print contents in window '{self.title}, exception: {e}")

        # Box (Border)
        if self.print_border: self.screen.box()

        # Window Title
        if self.print_title: self.screen.addstr(0, 1, f" {self.title} ")
