# editor.py

class Editor:
    def __init__(self, buffer, buff_w, buff_h):
        # Buffer
        self.buffer = buffer

        self.buff_w = buff_w # Terminal width in cols
        self.buff_h = buff_h # Terminal height in rows

        self.buff_x = 0 # Buffer horizontal position (scrolling)
        self.buff_y = 0 # Buffer vertical position (scrolling)

        self.buff_scrollv_offset = 5 # row offset for where vertical scrolling begins
        self.buff_scrollh_offset = 10 # col offset for where horizontal scrolling begins

        # Cursor
        self.curs_x = 0 # Cursor position (col)
        self.curs_y = 0 # Cursor position (row)
        self.curs_hint = 0 # Maintain curs_x when changing lines

        self.curs_offset_x = 0 # curs_x minimum value offset
        self.curs_offset_y = 0 # curs_y minimum value offset

    # Buffer Properties
    @property
    def buff_bottom(self):
        return self.buff_y + self.buff_h - 1

    @property
    def buff_right(self):
        return self.buff_x + self.buff_w - 1

    # Vertical Scrolling
    def buff_scroll_vert(self):
        if self.curs_y == (self.buff_y + self.buff_scrollv_offset) - 1 and self.buff_y > 0:
            self.buff_y -= 1
            return
        if self.curs_y == (self.buff_bottom - self.buff_scrollv_offset) + 1 and self.buff_bottom < len(self.buffer) - 1:
            self.buff_y += 1
            return

    # Horizontal Scrolling
    def buff_scroll_horiz(self):
        if self.curs_x == (self.buff_x + self.buff_scrollh_offset) - 1 and self.buff_x > 0:
            self.buff_x -= 1
            return
        if self.curs_x == (self.buff_right - self.buff_scrollh_offset) + 1 and self.buff_right < len(self.buffer[self.curs_y]) - 1:
            self.buff_x += 1
            return

    # Cursor Position -> Buffer Position Translation
    def translate_curs(self):
        return self.curs_y - self.buff_y, self.curs_x - self.buff_x

    # Cursor Movement
    def move_cursor(self, key):
        if key == 'h': # Left
            if self.curs_x > self.curs_offset_x:
                self.curs_x -= 1
                self.curs_hint = self.curs_x
                self.buff_scroll_horiz()
        if key == 'l': # Right
            if self.curs_x < len(self.buffer[self.curs_y]) - 1:
                self.curs_x += 1
                self.curs_hint = self.curs_x
                self.buff_scroll_horiz()
        if key == 'k': # Up
            if self.curs_y > self.curs_offset_y:
                self.curs_y -= 1
                self.curs_x = min(self.curs_hint, len(self.buffer[self.curs_y]) - 1)
                self.buff_scroll_vert()
        if key == 'j': # Down
            if self.curs_y < len(self.buffer) - self.curs_offset_y - 1:
                self.curs_y += 1
                self.curs_x = min(self.curs_hint, len(self.buffer[self.curs_y]) - 1)
                self.buff_scroll_vert()
