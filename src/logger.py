# Ink Editor - logger.py
# github.com/leftbones/ink

import os
from datetime import datetime

class Logger:
    def __init__(self, logfile):
        self.logfile = logfile

    def delete(self):
        try: os.remove(self.logfile)
        except: pass

    def erase(self):
        open(self.logfile, 'w').close()

    def write(self, message):
        time = datetime.now()
        str_time = time.strftime("%H:%M:%S")
        with open(self.logfile, 'a') as f:
            f.write(f"[{str_time}] {message}\n")

log = Logger("inklog.txt")
