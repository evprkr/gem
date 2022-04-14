class PopupWindow:
    def __init__(self, row, col, title, buffer=None, anchor=None):
        self.row = row
        self.col = col
        self.title = title
        self.buffer = buffer
        self.anchor = anchor

    def update(self, screen, cursor):
        # Height + Width
        height = self.buffer.rows
        width = self.buffer.cols

        # Anchor
        if self.anchor == "center":
            row = self.row - (height // 2)
            col = self.col - (width // 2)
        elif self.anchor == "bottom right":
            row = self.row - height
            col = self.col - width
        else:
            row = self.row
            col = self.col

        r_offset = row
        c_offset = col

        # Window + Box
        window = screen.derwin(height+3, width+2, row-1, col-1)
        window.box()

        # Title
        window.addstr(0, 1, f" {self.title} ")

        # Background
        for r in range(0, height):
            for c in range(0, width):
                screen.addstr(row+r, col+c, ' ')

        # Buffer
        if self.buffer:
            self.buffer.update(screen, cursor, r_offset, c_offset)
#            for row, line in enumerate(self.buffer.lines):
#                screen.addstr(row, col, line)
