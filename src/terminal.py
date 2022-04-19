from logger import *
from buffer import *
from popup import *
from input import *

class Terminal:
    def __init__(self, rows, cols, screen, cursor):
        self.rows = rows
        self.cols = cols
        self.screen = screen
        self.cursor = cursor

        self.windows = []
        self.buffers = []

        self.quit = False

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
        if steal_focus: self.cursor.buffer = window.buffer
        self.windows.append(window)
        self.buffers.append(window.buffer)
        #log.write(f"Terminal: new window created, buffer '{window.buffer.name}' added to buffers.")

    # Cycle focus between buffers
    def cycle_buffers(self):
        if len(self.buffers) == 1: return

        buff_idx = self.buffers.index(self.cursor.buffer)
        try: self.cursor.buffer = self.buffers[buff_idx + 1]
        except: self.cursor.buffer = self.buffers[0]

        self.cursor.row = 0 # TODO store position in buffer and restore when switching, set to 0, 0 if not stored
        self.cursor.col = 0

    # Update everything in the terminal
    def update(self):
        self.update_buffers()
        self.update_windows()
        self.screen.move(*self.cursor.buffer.translate_pos(self.cursor))

    # Update all buffers in the terminal
    def update_buffers(self):
        #log.write("Terminal: updating buffers...")
        self.screen.erase()
        for buffer in self.buffers:
            if buffer.window == self:
                buffer.update(self.cursor)
                #log.write(f"Buffer '{buffer.name}' updated successfully")

    # Update all windows in the terminal
    def update_windows(self):
        #log.write("Terminal: updating windows...")
        for window in self.windows:
            window.update()

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
        if keys[1] == None:
            key = keys[0]

            # Normal Mode
            if self.cursor.mode == "NORMAL":
                # Important Keys
                if key == Key.ModeInsert:
                    self.cursor.mode = "INSERT"

                elif key == Key.Delete or key == Key.InsDelete:
                    self.cursor.buffer.delete_char(self.cursor)
                    self.cursor.buffer.update_history(self.cursor)

                # Cursor Movement
                elif key == Key.CursorLeft: self.cursor.left()
                elif key == Key.CursorRight: self.cursor.right()
                elif key == Key.CursorUp: self.cursor.up()
                elif key == Key.CursorDown: self.cursor.down()

                elif key == Key.JumpLineStart: self.cursor.goto(self.cursor.row, 0)
                elif key == Key.JumpLineEnding: self.cursor.goto(self.cursor.row, self.cursor.line_end)

                elif key == Key.NextWordEnding:
                    if self.cursor.char == ' ': self.cursor.right()
                    while self.cursor.char not in ' \n': self.cursor.right()
                elif key == Key.PrevWordEnding:
                    if self.cursor.char == ' ': self.cursor.left()
                    while self.cursor.char not in ' ' and self.cursor.col > 0: self.cursor.left()

                elif key == Key.NextBlankLine:
                    if self.cursor.line == '\n': self.cursor.down()
                    while self.cursor.row < self.cursor.buffer.line_count-1 and self.cursor.line != '\n':
                        self.cursor.down()
                elif key == Key.PrevBlankLine:
                    if self.cursor.line == '\n': self.cursor.up()
                    while self.cursor.row > 0 and self.cursor.line != '\n':
                        self.cursor.up()

                elif key == Key.BufferLastRow:
                    self.cursor.goto(self.cursor.buffer.line_count-1, self.cursor.col)

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
            elif self.cursor.mode == "INSERT":
                if key in Key.Escape:
                    self.cursor.buffer.update_history(self.cursor)
                    self.cursor.mode = "NORMAL"
                    self.cursor.left()

                elif key in Key.Backspace: self.cursor.buffer.backspace(self.cursor)
                elif key == Key.InsDelete: self.cursor.buffer.delete_char(self.cursor)

                elif key == Key.Tab:
                    for i in range(4): self.cursor.buffer.insert_char(self.screen, self.cursor, ' ')
                elif key == '\n': self.cursor.buffer.split_line(self.cursor)

                else: self.cursor.buffer.insert_char(self.screen, self.cursor, key)

        # Leader Sequences
        elif keys[0] == Key.Leader:
            if keys == Seq.Quit: self.quit = True; log.write("Terminal: quit flag enabled")
            elif keys == Seq.Save: self.save_buffer(self.cursor.buffer)

        # Other Sequences
        elif len(keys) == 2:
            if keys == Seq.BufferFirstRow: self.cursor.goto(0, self.cursor.col)
            elif keys == Seq.LineDelete:
                self.cursor.buffer.delete_line(self.cursor)
                self.cursor.buffer.update_history(self.cursor)

            elif keys[0] == Wait.Replace:
                self.cursor.buffer.delete_char(self.cursor)
                self.cursor.buffer.insert_char(self.screen, self.cursor, keys[1])
                self.cursor.buffer.update_history(self.cursor)
