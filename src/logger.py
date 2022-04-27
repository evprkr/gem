import os
from datetime import datetime

class Logger:
    def __init__(self, logfile):
        self.logfile = logfile

    # Delete the log file
    def delete(self):
        try: os.remove(self.logfile)
        except: pass

    # Erase the log file
    def erase(self):
        open(self.logfile, 'w').close()

    # Write a message to the end of the log file
    def write(self, message):
        time = datetime.now()
        str_time = time.strftime("%H:%M:%S")
        with open(self.logfile, 'a') as f:
            f.write(f"[{str_time}] {message}\n")

log = Logger("inklog.txt")
