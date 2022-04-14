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

        self.buffers = []
        self.windows = []

        self.quit = False

    # Add buffer to the terminal
    def add_buffer(self, name, contents=[]):
        buffer = Buffer(name, self.rows, self.cols, contents)
        self.buffers.append(buffer)
        log.write(f"Buffer '{name}' added to Terminal")

        # If the cursor has no active buffer, set it to this one
        if self.cursor.buffer == None:
            self.cursor.buffer = self.buffers[-1]

    # Add window to the terminal
    def add_window(self, row, col, title, buffer=None, anchor=None):
        window = PopupWindow(row, col, title, buffer, anchor)
        if buffer: self.cursor.buffer = buffer
        self.windows.append(window)
        log.write("New window created in Terminal")

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
            buffer.update(self.screen, self.cursor)
            #log.write(f"Buffer '{buffer.name}' updated successfully")

    # Update all windows in the terminal
    def update_windows(self):
        #log.write("Terminal: updating windows...")
        for window in self.windows:
            window.update(self.screen, self.cursor)

    # Save contents of buffer to a file
    def save_buffer(self, buffer):
        contents = buffer.lines
        f = open(buffer.name, 'w')
        f.writelines(contents)
        f.close()
        buffer.dirty = False
        log.write(f"Buffer '{buffer.name}' saved successfully")

    # Process key(s) passed from stdin
    def process_input(self, keys):
        # Single Keys
        if keys[1] == None:
            key = keys[0]

            # Normal Mode
            if self.cursor.mode == "NORMAL":
                if key == Key.ModeInsert: self.cursor.mode = "INSERT"; log.write("Cursor mode set to INSERT")

                elif key == Key.Delete or key == Key.InsDelete: self.cursor.buffer.delete_char(self.cursor)

                elif key == Key.CursorLeft: self.cursor.left()
                elif key == Key.CursorRight: self.cursor.right()
                elif key == Key.CursorUp: self.cursor.up()
                elif key == Key.CursorDown: self.cursor.down()

                elif key == Key.LineDelete: self.cursor.buffer.delete_line(self.cursor)
                elif key == Key.LineAppend: self.cursor.goto(self.cursor.row, self.cursor.line_end, "INSERT")

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

            # Insert Mode
            elif self.cursor.mode == "INSERT":
                if key in Key.Escape: self.cursor.mode = "NORMAL"; log.write("Cursor mode set to NORMAL")
                elif key in Key.Backspace: self.cursor.buffer.backspace(self.cursor)
                elif key == Key.InsDelete: self.cursor.buffer.delete_char(self.cursor)
                elif key == '\n': self.cursor.buffer.split_line(self.cursor)
                else: self.cursor.buffer.insert_char(self.screen, self.cursor, key)

                # Update Buffer History
                if key not in Key.Escape: self.cursor.buffer.update_history()

        # Leader Sequences
        elif keys[0] == Key.Leader:
            if keys == Seq.Quit: self.quit = True; log.write("Terminal exit flag enabled")
            elif keys == Seq.Save: self.save_buffer(self.cursor.buffer)
