# statusline.py

class Statusline:
    def __init__(self, buffer):
        self.buffer = buffer # Which buffer this statusline belongs to

    def update(self, cursor):
        statusline = f"= {cursor.mode} "

        # Get percentage of the way the cursor is from the top of the buffer to the bottom
        percent = str(100 * ((cursor.row+1) / (self.buffer.line_count()))).split('.')[0] + "%"
        if cursor.row == self.buffer.line_count()-1: percent = "BOT"
        if cursor.row == 0: percent = "TOP"

        # Calculate spaces needed to fill the middle of the statusline
        spaces = self.buffer.cols - (len(cursor.mode) + len(str(cursor.col)) + len(str(cursor.row)) + len(percent) + 12)

        for i in range(spaces):
            statusline += "="

        statusline += f" {percent} = {cursor.col}, {cursor.row} ="

        return statusline
