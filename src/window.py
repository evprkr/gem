# Ink Editor - window.py
# github.com/leftbones/ink

import curses

from logger import log

from highlighter import Highlighter


class Window:
    def __init__(self, parent, wid, title, contents, row, col, nrows, ncols, box, margins, statusline, linenumbers, emptylines, readonly, lifetime):
        self.parent = parent
        self.wid = wid
        self.title = title
        self.contents = contents
        self.row = row
        self.col = col
        self.nrows = nrows
        self.ncols = ncols
        self.box = box
        self.margins = margins
        self.screen = self.parent.screen.derwin(self.nrows, self.ncols, self.row, self.col)

        self.row_offset = 0
        self.col_offset = 0

        self.cursor_mode = "NORMAL"
        self.cursor_row = 0
        self.cursor_col = 0

        self.path = None
        self.dirty = False

        self.lifetime = lifetime

        # "Dynamic" Configs - Can be set during window creation, falls back to inkrc file or default values
        self.statusline = statusline
        self.linenumbers = linenumbers
        self.emptylines = emptylines
        self.readonly = readonly

        # "Static" Configs - Set by the settings found in the inkrc file or default values
        self.hlsyntax = self.parent.config.hlsyntax
        self.tabstop = self.parent.config.tabstop
        self.autotabs = self.parent.config.autotabs
        self.bksptabs = self.parent.config.bksptabs
        self.deltabs = self.parent.config.deltabs
        self.vscrolloffset = self.parent.config.vscrolloffset
        self.hscrolloffset = self.parent.config.hscrolloffset

        # Syntax Highlighting
        self.language = None
        self.highlighter = Highlighter(self)

        # Calculate Margins
        self.upper_edge = 0 + self.margins[0]
        self.lower_edge = 0 + self.margins[1]
        self.left_edge = 0 + self.margins[2]
        self.right_edge = 0 + self.margins[3]

        if self.box:
            self.upper_edge += 1
            self.lower_edge += 1
            self.left_edge += 1
            self.right_edge += 1

        if self.linenumbers:
            self.left_edge += 6

    @property
    def bottom(self):
        return self.row_offset + (self.nrows - self.lower_edge)

    @property
    def right(self):
        return (self.col_offset + self.ncols) - self.left_edge

    @property
    def line_count(self):
        return len(self.contents)

    # Insert a character at the cursor position
    def insert_char(self, cursor, char):
        if self.readonly: return
        if not self.dirty: self.dirty = True
        cur_line = self.contents.pop(cursor.row)
        new_line = cur_line[:cursor.col] + char + cur_line[cursor.col:]
        self.contents.insert(cursor.row, new_line)
        cursor.move_right()

    # Replace the character under the cursor
    def replace_char(self, cursor, char):
        if self.readonly: return
        if not self.dirty: self.dirty = True

        self.delete_char(cursor)
        self.insert_char(cursor, char)

    # Delete the character under the cursor
    def delete_char(self, cursor):
        if self.readonly: return
        if not self.dirty: self.dirty = True
        row, col = cursor.row, cursor.col
        if (row, col) < (len(self.contents) - 1, len(self.contents[row]) - 1):
            if col < len(self.contents[row]) - 1:
                cur_line = self.contents.pop(row)
                new_line = cur_line[:col] + cur_line[col + 1:]
                self.contents.insert(row, new_line)
            else:
                cur_line = self.contents.pop(row)
                next_line = self.contents.pop(row)
                new_line = cur_line[:-1] + next_line
                self.contents.insert(row, new_line)

    # Delete the character left of the cursor
    def bksp_char(self, cursor):
        if self.readonly: return
        if not self.dirty: self.dirty = True
        row, col = cursor.row, cursor.col
        if col == 0:
            if row == 0: return

            cur_line = self.contents.pop(row)
            prev_line = self.contents.pop(row - 1)
            new_line = prev_line[:-1] + cur_line
            self.contents.insert(row - 1, new_line)

            cursor.row -= 1
            cursor.goto(row - 1, len(prev_line) - 1)
            self.scroll(cursor) # May not be necessary to call this here
        else:
            if self.contents[row][col - 4:col] == ' ' * self.tabstop:
                for i in range(self.tabstop):
                    cursor.move_left()
                    self.delete_char(cursor)
            else:
                cursor.move_left()
                self.delete_char(cursor)

    # Delete the line under the cursor
    def delete_line(self, cursor):
        if self.readonly: return
        if not self.dirty: self.dirty = True
        if cursor.row == len(self.contents) - 1: cursor.move_up()

        if cursor.window.line_count > 1: self.contents.pop(cursor.row)
        else: self.contents[cursor.row] = '\n'

        cursor.goto(cursor.row, 0)

    # Split line at cursor position, moves the second half to the next line and the cursor moves with it
    def split_line(self, cursor):
        if self.readonly: return
        if not self.dirty: self.dirty = True
        if self.line_count == 9999: return
        row, col = cursor.row, cursor.col
        cur_line = self.contents.pop(row)
        self.contents.insert(row, cur_line[:col] + '\n')
        self.contents.insert(row + 1, cur_line[col:])

        # Match current line's tabstops on the next line (config.autotab)
        if cur_line.startswith(' '):
            tabs = 0
            i = 0
            while cur_line[i] == ' ':
                if i % self.tabstop == 0: tabs += 1
                i += 1

            if tabs > 0:
                cursor.col_hint = tabs * self.tabstop
                cursor.move_down()
                for i in range(tabs * self.tabstop):
                    self.insert_char(cursor, ' ')
        else:
            cursor.col_hint = 0
            cursor.move_down()

    # Strip extraneous whitespace from lines
    def clean_lines(self, cursor):
        contents_copy = self.contents.copy()
        for row, line in enumerate(contents_copy):
            if line.isspace():
                self.contents[row] = '\n'
                if row == cursor.row: cursor.goto(row, 0)
            else: self.contents[row] = line.rstrip()
            if not self.contents[row].endswith('\n'): self.contents[row] += '\n'

    # Print window contents to the screen
    def print(self):
        # Background
        self.screen.bkgd(' ', curses.color_pair(self.parent.colorizer.get_pair()))

        for row in range(self.nrows):
            for col in range(self.ncols):
                self.screen.delch(row, col)
                self.screen.insch(row, col, ' ')

        # Empty Line Chars
        if self.emptylines:
            for row in range(self.upper_edge + len(self.contents), self.nrows):
                self.screen.insch(row, 1, '~', curses.A_DIM)

        # Contents + Line Numbers
        for row, line in enumerate(self.contents[self.row_offset:self.row_offset + (self.nrows - self.lower_edge - 1)]):
            if self.linenumbers:
                line_num = " " * (5 - len(str(row + self.row_offset + 1))) + str(row + self.row_offset + 1)

                if row == self.cursor_row - self.row_offset: self.screen.insstr(self.upper_edge + row, 1, line_num)
                else: self.screen.insstr(self.upper_edge + row, 1, line_num, curses.A_DIM)

            line_text = line[self.col_offset:self.col_offset + self.ncols - self.left_edge]

            if self.cursor_mode == "LIST" and (self.parent.sidebar_window == self or self.parent.tabswitcher_window == self):
                if row == self.cursor_row: self.screen.insstr(self.upper_edge + row, self.left_edge, line_text, curses.A_STANDOUT)
                else: self.screen.insstr(self.upper_edge + row, self.left_edge, line_text)
            elif self.hlsyntax:
                formatted_text = self.highlighter.format_text(line_text)
                self.parent.colorizer.print_syntax(self, self.upper_edge + row, self.left_edge, formatted_text)
            else:
                self.screen.insstr(self.upper_edge + row, self.left_edge, line_text)

            # Selection Highlight
            if self.cursor_mode == "SELECT":
                start_row = self.parent.cursor.sel_start_row
                start_col = self.parent.cursor.sel_start_col

                if row + self.row_offset + 1 == start_row:
                    if self.cursor_row + 1 == start_row:
                        for col, char in enumerate(line_text):
                            if start_col - 1 <= col <= self.cursor_col:
                                self.screen.chgat(row + 1, col + self.left_edge, 1, curses.color_pair(self.parent.colorizer.get_pair(self.parent.colorizer.default_fg, self.parent.colorizer.highlight_bg)))
                    else:
                        for col, char in enumerate(line_text):
                            if col >= start_col - 1:
                                self.screen.chgat(row + 1, col + self.left_edge, 1, curses.color_pair(self.parent.colorizer.get_pair(self.parent.colorizer.default_fg, self.parent.colorizer.highlight_bg)))
                elif row + self.row_offset + 1 == self.cursor_row + 1:
                    for col, char in enumerate(line_text):
                        if col <= self.cursor_col - 1:
                            self.screen.chgat(row + 1, col + self.left_edge, 1, curses.color_pair(self.parent.colorizer.get_pair(self.parent.colorizer.default_fg, self.parent.colorizer.highlight_bg)))
                elif start_row <= row + self.row_offset + 1 <= self.cursor_row + 1:
                    for col, char in enumerate(line_text):
                        self.screen.chgat(row + 1, col + self.left_edge, 1, curses.color_pair(self.parent.colorizer.get_pair(self.parent.colorizer.default_fg, self.parent.colorizer.highlight_bg)))

        # Box
        if self.box:
            self.screen.box()
            self.screen.delch(0, 0)
            self.screen.delch(0, self.ncols - 1)
            self.screen.delch(self.nrows - 1, 0)
            self.screen.delch(self.nrows - 1, self.ncols - 1)
            self.screen.insstr(0, 0, "╭")
            self.screen.insstr(0, self.ncols - 1, "╮")
            self.screen.insstr(self.nrows - 1, 0, "╰")
            self.screen.insstr(self.nrows - 1, self.ncols - 1, "╯")

        # Title
        if self.title:
            if self.dirty and self.parent.prompt_window != self: self.screen.addstr(0, 1, f" {self.title} + ")
            else: self.screen.addstr(0, 1, f" {self.title} ")

        # Status
        if self.statusline:
            cursor_pos = f" {self.cursor_row + 1}:{self.cursor_col + 1} "

#            if self.cursor_row == 0: window_pos = " top "
#            elif self.cursor_row == self.line_count - 1: window_pos = " bot "
            window_pos = f" {int((float(self.cursor_row + 1) / float(self.line_count)) * 100)}% "

            language = f" {self.language} "
            self.screen.addstr(self.nrows - 1, self.ncols - (len(cursor_pos) + 1), cursor_pos)
            self.screen.addstr(self.nrows - 1, self.ncols - ((len(cursor_pos) + 1) + (len(window_pos) + 1)), window_pos)
            self.screen.addstr(self.nrows - 1, self.ncols - ((len(cursor_pos) + 1) + (len(window_pos) + 1) + (len(language) + 1)), language)

            cursor_mode = f" {self.cursor_mode} "
            self.screen.addstr(self.nrows - 1, 1, cursor_mode)

        # Lifetime
        if self.lifetime > 0:
            lifetime = f" {int(self.lifetime / 2)} "
            self.screen.addstr(0, self.ncols - len(lifetime) - 1, lifetime)

    # Translate the cursor position in the screen to the cursor relative position in the current window
    def translate_pos(self, cursor):
        return (
            self.row + (cursor.row - self.row_offset) + self.upper_edge,
            self.col + (cursor.col - self.col_offset) + self.left_edge
        )

    # Scroll the window contents vertically or horizontally
    def scroll(self, cursor):
        while cursor.row <= (self.row_offset + self.vscrolloffset) - 1 and self.row_offset > 0: self.row_offset -= 1
        while cursor.row >= (self.bottom - self.vscrolloffset) + 1 and self.bottom < len(self.contents) + self.lower_edge: self.row_offset += 1

        while cursor.col <= (self.col_offset + self.hscrolloffset) - 1 and self.col_offset > 0: self.col_offset -= 1
        while cursor.col >= (self.right - self.hscrolloffset) - 1: self.col_offset += 1
