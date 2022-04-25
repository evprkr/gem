import curses
from logger import *
from input import *
from history import History

class Buffer:
    def __init__(self, name, lines, window=None, rows=None, cols=None, border=False, title=True, scroll_offsets=(5, 10)):
        self.name = name
        self.lines = lines
        self.window = window

        if not rows: self.rows = len(self.lines)
        else: self.rows = rows

        if not cols: self.cols = len(max(self.lines, key=len)) + 2
        else: self.cols = cols

        self.dirty = False
        self.history = History()

        self.widgets = []

        # Cursor Memory
        self.cursor_row = 0
        self.cursor_col = 0

        # Buffer Settings
        self.editable = True        # Contents (lines) are mutable, defaults to `True`
        self.focusable = True       # Buffer can be focused by the cursor, defaults to `True`
        self.scrollable_v = True    # Buffer can be scrolled vertically if rows exceeds the height, defaults to `True`
        self.scrollable_h = True    # Buffer can be scrolled horizontall if cols exceeds the width, defaults to `True`
        self.line_numbers = True    # Line numbers should be drawn (shifts contents +3 cols), defaults to `True`
        self.empty_lines = True     # Empty lines (outside the buffer) should be indicated with a `~`, defaults to `True`
        self.border = border        # Border box should be drawn around the buffer
        self.title = title          # Print the buffer name at the top left of the border

        # Margins and Offsets
        self.row_offset = 0 # Vertical scroll offset
        self.col_offset = 0 # Horizontal scroll offset

        self.scroll_offset_v = scroll_offsets[0] # TODO Move these elsewhere, they don't belong here (ink_config.py?)
        self.scroll_offset_h = scroll_offsets[1]

        # Text Position Offsets
        self.margin_top = 0
        self.margin_bottom = 0
        self.margin_left = 0
        self.margin_right = 0

        # Cursor Position Offset
        self.row_shift = 0
        self.col_shift = 0

    def __repr__(self):
        return f"[Buffer: '{self.name}' ({self.rows}, {self.cols}), {self.line_count} lines]"

    @property
    def bottom(self):
        return self.row_offset + (self.rows - self.margin_bottom) - self.border

    @property
    def right(self):
        return (self.col_offset + self.cols) - self.margin_left - self.line_numbers

    @property
    def line_count(self):
        return len(self.lines)


    # Update buffer contents on the terminal screen
    def update(self, cursor):
        # Update Margins
        self.margin_top = 0
        self.margin_bottom = 0
        self.margin_left = 0
        self.margin_right = 0

        if self.line_numbers: self.margin_left += 6

        if self.border:
            self.margin_top += 1
            self.margin_bottom += 1
            self.margin_left += 2
            self.margin_right += 2

        # Print background
        for r in range(0, self.rows):
            for c in range(0, self.cols):
                self.window.screen.insch(r, c, ' ')

        # Print empty line chars
        if self.empty_lines:
            for i in range(0, self.rows):
                self.window.screen.addstr(i, self.border, '~', curses.A_DIM)

        # Print line numbers + contents
        for row, line in enumerate(self.lines[self.row_offset:self.row_offset + (self.rows - self.margin_bottom)]):
            if self.line_numbers:
                line_number = f"{row + self.row_offset + 1}"
                for i in range((self.margin_left - 1) - len(line_number)):
                    line_number = " " + line_number

                # Highlight current line number in active buffer
                if cursor.buffer == self and row == cursor.row - self.row_offset: self.window.screen.addstr(row + self.margin_top, 0, line_number)
                else: self.window.screen.addstr(row + self.margin_top, 0, line_number, curses.A_DIM)

            line_text = line[self.col_offset:self.col_offset + self.cols - self.margin_left]
            self.window.screen.addstr(row + self.margin_top, self.margin_left, line_text)

        # Print border
        if self.border:
            self.window.screen.box()
            if self.title: self.window.screen.addstr(0, 1, f" {self.name} ")

        # Update + Print all widgets
        for widget in self.widgets:
            widget_lines = widget.update()
            for row, line in enumerate(widget_lines):
                self.window.screen.addstr(widget.row, widget.col, *widget.update())


    # Translate cursor position relative to buffer offets
    def translate_pos(self, cursor):
        return (((cursor.row - self.row_offset) + self.margin_top) + self.row_shift,
                ((cursor.col - self.col_offset) + self.margin_left) + self.col_shift)

    # Get a specific line from the buffer
    def get_line(self, row):
        return self.lines[row]

    # Resize buffer
    def resize(self, rows, cols):
        self.rows = rows
        self.cols = cols

    # Add a new widget to the buffer
    def add_widget(self, widget):
        self.widgets.append(widget)
        log.write(f"Buffer: widget {widget.name} added to Buffer '{self.name}'")

    # Remove a widget from the buffer
    def remove_widget(self, widget):
        self.widgets.remove(widget)
        log.write(f"Buffer: widget {widget.name} removed from Buffer '{self.name}'")

    # Update history
    def update_history(self, cursor):
        if not self.editable: return
        if self.history.index > 0: self.history.fork()
        lines_copy = self.lines.copy()
        self.history.add(cursor, lines_copy)

    # Strip unnecessary whitespace from lines
    def clean_lines(self, cursor):
        lines_copy = self.lines.copy()

        for row, line in enumerate(lines_copy):
            if line.isspace():
                self.lines[row] = '\n'
                if row == cursor.row: cursor.goto(row, 0)
            else: self.lines[row] = line.rstrip()
            
            if not self.lines[row].endswith('\n'): self.lines[row] += '\n'

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

    # Replace character under cursor
    def replace_char(self, cursor, screen, char):
        if not self.editable: return
        if not self.dirty: self.dirty = True

        self.delete_char(cursor)
        self.insert_char(self.screen, self.cursor, keys[1])
        cursor.buffer.update_history(self.cursor)

    # Delete the entire line under the cursor
    def delete_line(self, cursor):
        if not self.editable: return
        if not self.dirty: self.dirty = True

        if cursor.row == len(self.lines) - 1: cursor.up()

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
        if self.line_count == 9999: return
        row, col = cursor.row, cursor.col
        cur_line = self.lines.pop(row)
        self.lines.insert(row, cur_line[:col]+'\n')
        self.lines.insert(row + 1, cur_line[col:])

        # Match current line's tabs on the next line
        if cur_line.startswith(' '):
            tabs = 0
            i = 0
            while cur_line[i] == ' ':
                if i % 4 == 0: tabs += 1
                i += 1
           
            if tabs > 0:
                cursor.hint = tabs * 4
                cursor.down()
                for i in range(tabs * 4):
                    self.insert_char(self.window.screen, cursor, ' ')
        else:
            cursor.hint = 0
            cursor.down()

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

    # Scrolling
    def scroll(self, cursor, center=False):
        # Update Cursor Memory
        self.cursor_row = cursor.row
        self.cursor_col = cursor.col

        if self.scrollable_v:
            while cursor.row <= (self.row_offset + self.scroll_offset_v) - 1 and self.row_offset > 0: self.row_offset -= 1
            while cursor.row >= (self.bottom - self.scroll_offset_v) + 1 and self.bottom < len(self.lines) - 1: self.row_offset += 1

        if self.scrollable_h:
            while cursor.col <= (self.col_offset + self.scroll_offset_h) - 1 and self.col_offset > 0: self.col_offset -= 1
            while cursor.col >= (self.right - self.scroll_offset_h) - 1: self.col_offset += 1

        # TODO Center buffer scroll offset on cursor if `center` flag is enabled
        if center: pass
