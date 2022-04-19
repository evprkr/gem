import curses
import platform
from logger import *
from input import *
from history import History

class Buffer:
    def __init__(self, name, lines, window=None, rows=None, cols=None):
        self.name = name
        self.lines = lines
        self.window = window

        if not rows: self.rows = len(self.lines)
        else: self.rows = rows

        if not cols: self.cols = len(max(self.lines, key=len)) + 2
        else: self.cols = cols

        self.editable = True        # If contents (lines) are mutable, defaults to `True`
        self.line_numbers = True    # If line numbers should be drawn (shifts contents +3 cols), defaults to `True`
        self.empty_lines = True     # If empty lines (outside the buffer) should be indicated with a `~`, defaults to `True`
        self.status_line = True     # If a statusline should be drawn (covers the last row of the buffer)

        self.dirty = False
        self.history = History()

        self.row_offset = 0 # Vertical scroll offset
        self.col_offset = 0 # Horizontal scroll offset

        self.scroll_offset_v = 5 # TODO Move these elsewhere, they don't belong here (gem_config.py?)
        self.scroll_offset_h = 10

        self.margin_left = 3 
        self.margin_bottom = 0

        self.row_shift = 0
        self.col_shift = 0

        self.prompt_open = False

        self.widgets = []

    def __repr__(self):
        return f"[Buffer: '{self.name}' ({self.rows}, {self.cols}), {self.line_count} lines]"

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
        return self.margin_bottom + (cursor.row - self.row_offset) + self.row_shift, self.margin_left + (cursor.col - self.col_offset) + self.col_shift

    # Get a specific line from the buffer
    def get_line(self, row):
        return self.lines[row]

    # Resize buffer
    def resize(self, rows, cols):
        self.rows = rows
        self.cols = cols

    # Update history
    def update_history(self, cursor):
        if not self.editable: return
        if self.history.index > 0: self.history.fork()
        lines_copy = self.lines.copy()
        self.history.add(cursor, lines_copy)

    # Undo last action
    def undo(self, cursor):
        if not self.editable: return
        if self.history.index + 1 < len(self.history.changes):
            action = self.history.undo()
            self.lines = action.items.copy()
            cursor.goto(*action.cursor_pos)

    # Redo last undone action
    def redo(self, cursor):
        if self.history.index > 0:
            action = self.history.redo()
            self.lines = action.items.copy()
            cursor.goto(*action.cursor_pos)
            self.scroll(cursor)

    # Update buffer contents on the terminal screen
    def update(self, cursor):
        # Print empty line chars
        if self.empty_lines:
            for i in range(self.rows):
                self.window.screen.addstr(i, 0, ' ~', curses.A_DIM)

        # Print lines from contents + line numbers (if enabled)
        for row, line in enumerate(self.lines[self.row_offset:self.row_offset + self.rows]):
            if self.line_numbers:
                line_number_offset = 3

                line_number = f"{row + self.row_offset + 1}"
                if row + self.row_offset + 1 < 10: line_number = " " + line_number

                if cursor.buffer == self and row == (cursor.row - self.row_offset): self.window.screen.addstr(row, 0, f"{line_number}")
                else: self.window.screen.addstr(row, 0, f"{line_number}", curses.A_DIM)
            else:
                line_number_offset = 2

            line_text = line[self.col_offset:self.col_offset + self.cols - line_number_offset]
            self.window.screen.addstr(row, line_number_offset, f"{line_text}")

        # Print the status line # TODO Turn this into a widget
        if self.status_line:
            for i in range(self.cols):
                self.window.screen.addstr(self.rows, i, ' ', curses.A_REVERSE)

            cursor_pos = f"{cursor.row+1}:{cursor.col+1}"
            cursor_mode = f" {cursor.mode} "

            try:
                if cursor.row == 0: buffer_pos = f"TOP "
                elif cursor.row == self.line_count-1: buffer_pos = f"BOTTOM "
                else: buffer_pos = f"{int((float(cursor.row) / float(self.line_count-1)) * 100)}% "
            except:
                buffer_pos = f"oops "

            if self.dirty: filename = f"{self.name} *"
            else: filename = f"{self.name}"

            self.window.screen.addstr(self.rows, 0, cursor_mode, curses.A_REVERSE | curses.A_BOLD)
            self.window.screen.addstr(self.rows, len(cursor_mode), filename, curses.A_REVERSE)
            self.window.screen.addstr(self.rows, self.cols-(len(cursor_pos)+1), cursor_pos, curses.A_REVERSE | curses.A_BOLD)
            self.window.screen.addstr(self.rows, self.cols-((len(cursor_pos)+1) + len(buffer_pos)), buffer_pos, curses.A_REVERSE)

        # Update and print all widgets
        for widget in self.widgets:
            self.window.screen.addstr(widget.row, widget.col, *widget.update())

    # Insert character at cursor position
    def insert_char(self, screen, cursor, char):
        if not self.editable: return
        if not self.dirty: self.dirty = True
        cur_line = self.lines.pop(cursor.row)
        new_line = cur_line[:cursor.col] + char + cur_line[cursor.col:]
        self.lines.insert(cursor.row, new_line)
        cursor.right()


    # Delete character under the cursor
    def delete_char(self, cursor):
        if not self.editable: return
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
        if not self.editable: return
        if not self.dirty: self.dirty = True
        if cursor.buffer.line_count > 1: self.lines.pop(cursor.row)
        else: self.lines[cursor.row] = '\n'
        cursor.goto(cursor.row, 0)

    # Backspace character left of the cursor
    def backspace(self, cursor):
        if not self.editable: return
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
        if not self.editable: return
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
        log.write(f"Buffer: widget {widget.name} added to Buffer '{self.name}'")

    # Remove a widget from the buffer
    def remove_widget(self, widget):
        self.widgets.remove(widget)
        log.write(f"Buffer: widget {widget.name} removed from Buffer '{self.name}'")

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
        while cursor.row > self.bottom:
            self.row_offset += 1

        while cursor.row < self.row_offset:
            self.row_offset -= 1

        while cursor.col > self.right:
            self.col_offset += 1

        while cursor.col < self.col_offset:
            self.col_offset -= 1

        # TODO Center buffer scroll offset on cursor if `center` flag is enabled
        if center: pass
