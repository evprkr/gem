from datetime import datetime

class Logger:
    def __init__(self, logfile):
        self.logfile = logfile

    def write(self, message):
        time = datetime.now()
        str_time = time.strftime("%m/%d/%Y, %H:%M:%S")
        with open(self.logfile, 'a') as f:
            f.write(f"[{str_time}] {message}\n")

log = Logger("gemlog.txt")
