import curses
import platform
from logger import *

class Buffer:
    def __init__(self, name, rows, cols, lines):
        self.name = name
        self.rows = rows
        self.cols = cols
        self.lines = lines

        self.dirty = False

        self.row_offset = 0
        self.col_offset = 0

        self.scroll_offset_v = 5 # TODO Move these elsewhere, they don't belong here
        self.scroll_offset_h = 10

        self.margin_left = 3
        self.margin_bottom = 0

        self.widgets = []

        self.history = []
        self.hist_idx = 0
        self.hist_max = 5

    @property
    def bottom(self):
        return self.row_offset + self.rows - 1

    @property
    def right(self):
        return self.col_offset + self.cols - 3

    @property
    def line_count(self):
        return len(self.lines)

    # Translate cursor position relative to buffer offets
    def translate_pos(self, cursor):
        return cursor.row - self.row_offset, self.margin_left + (cursor.col - self.col_offset)

    # Get a specific line from the buffer
    def get_line(self, row):
        return self.lines[row]

    # Update history
    def update_history(self):
        if len(self.history) > self.hist_max: self.history.pop(0)
        self.history.append(self.lines)
        self.hist_idx = len(self.history)

    # Undo last action
    def undo(self):
        self.hist_idx -= 1
        self.lines = self.history[self.hist_idx]

    # Redo last undone action
    def redo(self):
        pass
        #self.hist_idx += 1

    # Update buffer contents on the terminal screen
    def update(self, screen, cursor, r_offset=0, c_offset=0):
        # Print empty line chars
        for i in range(self.rows):
            screen.addstr(r_offset + i, c_offset + 0, ' ~')

        # Print lines from contents + line numbers
        for row, line in enumerate(self.lines[self.row_offset:self.row_offset + self.rows]):
            line_number = f"{row + self.row_offset + 1}"
            if row + self.row_offset + 1 < 10: line_number = " " + line_number

            screen.addstr(r_offset + row, c_offset + 0, f"{line_number}")

            line_text = line[self.col_offset:self.col_offset + self.cols - 3] # Note: this -3 is here to make the end of the line match the end of the statusline which can't print in the last col for some reason
            screen.addstr(r_offset + row, c_offset + 3, f"{line_text}")

        # Print the status line # TODO Turn this into a widget
        for i in range(self.cols):
            screen.addstr(r_offset + self.rows, c_offset + i, ' ', curses.A_REVERSE)

        cursor_pos = f"{cursor.row+1}:{cursor.col+1}"
        cursor_mode = f" {cursor.mode} "
        buffer_pos = f"{int((float(cursor.row) / float(self.line_count-1)) * 100)}% "
        if self.dirty: filename = f"{self.name} *"
        else: filename = f"{self.name}"

        screen.addstr(r_offset + self.rows, c_offset + 0, cursor_mode, curses.A_REVERSE | curses.A_BOLD)
        screen.addstr(r_offset + self.rows, c_offset + len(cursor_mode), filename, curses.A_REVERSE)
        screen.addstr(r_offset + self.rows, c_offset + self.cols-(len(cursor_pos)+1), cursor_pos, curses.A_REVERSE | curses.A_BOLD)
        screen.addstr(r_offset + self.rows, c_offset + self.cols-((len(cursor_pos)+1) + len(buffer_pos)), buffer_pos, curses.A_REVERSE)

        # Update and print all widgets
        for widget in self.widgets:
            screen.addstr(widget.row, widget.col, *widget.update())

    # Insert character at cursor position
    def insert_char(self, screen, cursor, char):
        if not self.dirty: self.dirty = True
        cur_line = self.lines.pop(cursor.row)
        new_line = cur_line[:cursor.col] + char + cur_line[cursor.col:]
        self.lines.insert(cursor.row, new_line)
        cursor.right()


    # Delete character under the cursor
    def delete_char(self, cursor):
        if not self.dirty: self.dirty = True
        row, col = cursor.row, cursor.col
        if (row, col) < (len(self.lines)-1, len(self.lines[row])-1):
            if col < len(self.lines[row]) - 1:
                cur_line = self.lines.pop(row)
                new_line = cur_line[:col] + cur_line[col + 1:]
                self.lines.insert(row, new_line)
            else:
                cur_line = self.lines.pop(row)
                next_line = self.lines.pop(row)
                new_line = cur_line[:-1] + next_line
                self.lines.insert(row, new_line)

    # Delete the entire line under the cursor
    def delete_line(self, cursor):
        if not self.dirty: self.dirty = True
        if cursor.buffer.line_count > 1: self.lines.pop(cursor.row)
        else: self.lines[cursor.row] = '\n'
        cursor.goto(cursor.row, 0)

    # Backspace character left of the cursor
    def backspace(self, cursor):
        if not self.dirty: self.dirty = True
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
            if self.lines[row][col-4:col] == '    ':
                for i in range(4):
                    cursor.left()
                    self.delete_char(cursor)
            else:
                cursor.left()
                self.delete_char(cursor)

    # Split line at cursor, moving the second half to the next line and the cursor with it
    def split_line(self, cursor):
        if not self.dirty: self.dirty = True
        row, col = cursor.row, cursor.col
        cur_line = self.lines.pop(row)
        self.lines.insert(row, cur_line[:col]+'\n')
        self.lines.insert(row + 1, cur_line[col:])
        cursor.hint = 0
        cursor.down()

    # Add a new widget to the buffer
    def add_widget(self, widget):
        self.widgets.append(widget)
        log.write(f"Widget {widget.name} added to Buffer '{self.name}'")

    # Remove a widget from the buffer
    def remove_widget(self, widget):
        self.widgets.remove(widget)
        log.write(f"Widget {widget.name} removed from Buffer '{self.name}'")

    # Scrolling
    def scroll(self, cursor, center=False):
        if cursor.row <= (self.row_offset + self.scroll_offset_v) - 1 and self.row_offset > 0:
            self.row_offset -= 1
        if cursor.row >= (self.bottom - self.scroll_offset_v) + 1 and self.bottom < len(self.lines) - 1:
            self.row_offset += 1
        if cursor.col == (self.col_offset + self.scroll_offset_h) - 1 and self.col_offset > 0:
            self.col_offset -= 1
        if cursor.col == (self.right - self.scroll_offset_h) + 1 and self.right < len(self.lines[cursor.row]) - 1:
            self.col_offset += 1

        # Scroll buffer to cursor when it goes outside the screen
        while cursor.col > self.right:
            self.col_offset += 1

        while cursor.col < self.col_offset:
            self.col_offset -= 1

        # TODO Center buffer scroll offset on cursor if `center` flag is enabled
        if center: pass
