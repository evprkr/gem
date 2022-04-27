from logger import *
from buffer import *
from popup import *
from input import *

from cmd_handler import CmdHandler

class Terminal:
    def __init__(self, rows, cols, screen, cursor):
        self.rows = rows
        self.cols = cols
        self.screen = screen
        self.cursor = cursor

        self.cmd_handler = CmdHandler(self)

        self.windows = []
        self.buffers = []

        self.quit = False
        self.delete_log = True # Deletes `inklog.txt` upon a successful exit

    def __repr__(self):
        return f"[Main Terminal, contains: '{self.buffers}' and '{self.windows}']"

    # Update everything in the terminal
    def update(self):
        self.update_buffers()
        self.screen.move(*self.cursor.buffer.translate_pos(self.cursor))

    # Update all buffers in the terminal
    def update_buffers(self):
        self.screen.erase()
        #log.write("Terminal: updating buffers...")
        for buffer in self.buffers:
            buffer.update(self.cursor)
            #log.write(f"Buffer '{buffer.name}' updated successfully")

    # Update all windows in the terminal
    def update_windows(self):
        #log.write("Terminal: updating windows...")
        for window in self.windows:
            window.update()

    # Add buffer to the terminal
    def add_buffer(self, buffer, fill=True):
        if fill: buffer.rows = self.rows
        if fill: buffer.cols = self.cols
        buffer.history.add(self.cursor, buffer.lines.copy())
        self.buffers.append(buffer)
        log.write(f"Terminal: buffer '{buffer.name}' added to Terminal")

        # If the cursor has no active buffer, set it to this one
        if self.cursor.buffer == None:
            self.cursor.buffer = self.buffers[-1]

    # Add window to the terminal
    def add_window(self, window, steal_focus=True):
        if steal_focus:
            self.cursor.buffer = window.buffer
            self.cursor.goto(0, 0)
        self.windows.append(window)
        self.buffers.append(window.buffer)
        #log.write(f"Terminal: new window created, buffer '{window.buffer.name}' added to buffers.")

    # Remove window from the terminal
    def remove_window(self, window):
        if self.cursor.buffer == window.buffer:
            self.cursor.buffer = self.cursor.prev_buffer
        self.windows.remove(window)
        self.buffers.remove(window.buffer)
        log.write("Terminal: window '{window.title}' removed from Terminal")

    # Create and enter a prompt window
    def open_prompt(self):
        self.cursor.prev_buffer = self.cursor.buffer
        self.cursor.mode = "PROMPT"
        cmd_buff = Buffer("Prompt", ['\n'], scrollable_v=False, line_numbers=False, empty_lines=False, border=True, statusline=False, scroll_offsets=(0, 0))
        cmd_buff.cols = self.cols // 3
        cmd_buff.rows = 2
        self.add_window(PopupWindow(self.rows//2, self.cols//2, "Prompt", cmd_buff, self.screen, "center"))
        log.write("Prompt window created")

    # Close the prompt and return focus to the previous buffer
    def close_prompt(self):
        try:
            prev_idx = self.buffers.index(self.cursor.prev_buffer)
            buff_idx = self.buffers.index(self.cursor.buffer)
            win_idx = self.windows.index(self.cursor.buffer.window)
            self.goto_buffer(prev_idx)
            self.buffers.pop(buff_idx)
            self.windows.pop(win_idx)
            self.cursor.mode = "NORMAL"
            log.write("Prompt window destroyed")
        except:
            log.write("Terminal: failed to close prompt, likely closed by CmdHandler")

    # Cycle focus between buffers
    def cycle_buffers(self):
        if len(self.buffers) == 1: return

        self.cursor.prev_buffer = self.cursor.buffer

        buff_idx = self.buffers.index(self.cursor.buffer)
        try: self.cursor.buffer = self.buffers[buff_idx + 1]
        except: self.cursor.buffer = self.buffers[0]

        self.cursor.goto(self.cursor.buffer.cursor_row, self.cursor.buffer.cursor_col)
        self.cursor.buffer.scroll(self.cursor)

    # Move cursor focus to specific buffer
    def goto_buffer(self, idx, row=None, col=None):
        self.cursor.buffer = self.buffers[idx]

        if not row: row = self.cursor.buffer.cursor_row
        if not col: col = self.cursor.buffer.cursor_col

        self.cursor.goto(row, col)
        self.cursor.buffer.scroll(self.cursor)

    # Save contents of buffer to a file
    def save_buffer(self, buffer):
        contents = buffer.lines
        f = open(buffer.name, 'w')
        f.writelines(contents)
        f.close()
        buffer.dirty = False
        log.write(f"Terminal: buffer '{buffer.name}' saved successfully")

    # Process key(s) passed from stdin
    def process_input(self, keys):
        # Single Keys
        # ------------------------------
        if keys[1] == None:
            key = keys[0]

            # Normal Mode
            # ------------------------------
            if self.cursor.mode == "NORMAL":
                # Important Keys
                if key == Key.ModeInsert:
                    self.cursor.mode = "INSERT"

                if key == Key.ModePrompt:
                    self.open_prompt()

                elif key == Key.Delete or key == Key.InsDelete:
                    self.cursor.buffer.delete_char(self.cursor)
                    self.cursor.buffer.update_history(self.cursor)

                # Cursor Movement
                elif key == Key.CursorLeft: self.cursor.left()
                elif key == Key.CursorRight: self.cursor.right()
                elif key == Key.CursorUp: self.cursor.up()
                elif key == Key.CursorDown: self.cursor.down()

                elif key == Key.JumpLineStart: self.cursor.goto(self.cursor.row, 0)
                elif key == Key.JumpLineEnding: self.cursor.goto(self.cursor.row, self.cursor.line_end - 1)

                elif key == Key.NextWordEnding:
                    if self.cursor.char == ' ': self.cursor.right()
                    while self.cursor.char not in ' \n': self.cursor.right()
                elif key == Key.PrevWordEnding:
                    if self.cursor.char == ' ': self.cursor.left()
                    while self.cursor.char not in ' ' and self.cursor.col > 0: self.cursor.left()

                elif key == Key.NextBlankLine:
                    if self.cursor.line == '\n': self.cursor.down()
                    while self.cursor.row < self.cursor.buffer.line_count - 1 and self.cursor.line != '\n':
                        self.cursor.down()
                elif key == Key.PrevBlankLine:
                    if self.cursor.line == '\n': self.cursor.up()
                    while self.cursor.row > 0 and self.cursor.line != '\n':
                        self.cursor.up()

                elif key == Key.BufferLastRow:
                    self.cursor.goto(self.cursor.buffer.line_count - 1, self.cursor.col)

                # Text Manipulation
                elif key == Key.LineAppend: self.cursor.goto(self.cursor.row, self.cursor.line_end, "INSERT"); 
                elif key == Key.LineDelete:
                    self.cursor.buffer.delete_line(self.cursor)
                    self.cursor.buffer.update_history(self.cursor)

                elif key == Key.UndoAction: self.cursor.buffer.undo(self.cursor)
                elif key == Key.RedoAction: self.cursor.buffer.redo(self.cursor)

                # Buffer Navigation
                elif key == Key.BufferCycle: self.cycle_buffers()

            # Insert Mode
            # ------------------------------
            elif self.cursor.mode == "INSERT":
                if key in Key.Escape:
                    self.cursor.buffer.clean_lines(self.cursor)
                    self.cursor.buffer.update_history(self.cursor)
                    self.cursor.mode = "NORMAL"
                    self.cursor.left()

                elif key in Key.Backspace: self.cursor.buffer.backspace(self.cursor)
                elif key == Key.InsDelete: self.cursor.buffer.delete_char(self.cursor)

                elif key == Key.ArrowLeft: self.cursor.left()
                elif key == Key.ArrowRight: self.cursor.right()
                elif key == Key.ArrowUp: self.cursor.up()
                elif key == Key.ArrowDown: self.cursor.down()

                elif key == Key.Tab:
                    for i in range(4): self.cursor.buffer.insert_char(self.screen, self.cursor, ' ')
                elif key in Key.Enter: self.cursor.buffer.split_line(self.cursor)

                else: self.cursor.buffer.insert_char(self.screen, self.cursor, key)

            # Prompt Mode
            # ------------------------------
            elif self.cursor.mode == "PROMPT":
                if key in Key.Escape: self.close_prompt()
                elif key == Key.ArrowLeft: self.cursor.left()
                elif key == Key.ArrowRight: self.cursor.right()
                elif key == Key.InsDelete: self.cursor.buffer.delete_char(self.cursor)
                elif key in Key.Backspace:
                    if self.cursor.col == 0: self.close_prompt()
                    else: self.cursor.buffer.backspace(self.cursor)

                elif key in Key.Enter:
                    error = self.cmd_handler.process(self.cursor.buffer.lines)
                    if error: log.write(f"Terminal: {error}") # TODO display error on screen and clear buffer
                    self.close_prompt()

                elif key in (Key.ArrowUp, Key.ArrowDown, Key.Tab): pass
                else: self.cursor.buffer.insert_char(self.screen, self.cursor, key)


        # Leader Sequences
        # ------------------------------
        elif keys[0] == Key.Leader:
            if keys == Seq.Save: self.save_buffer(self.cursor.buffer)

        # Other Sequences
        # ------------------------------
        elif len(keys) == 2:
            if keys == Seq.ForceQuit: self.quit = True; log.write("Terminal: quit flag enabled")
            elif keys == Seq.BufferFirstRow: self.cursor.goto(0, self.cursor.col)
            elif keys == Seq.LineDelete:
                self.cursor.buffer.delete_line(self.cursor)
                self.cursor.buffer.update_history(self.cursor)

            elif keys[0] == Wait.Replace:
                self.cursor.buffer.replace_char(self.cursor, keys[1])
