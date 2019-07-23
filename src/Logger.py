from datetime import datetime
from colorama import Fore, Back, Style

class Logger:
    def __init__(self):
        self.logfile = "dateless.txt"
        pass

    def log(self, statement, type='default'):
        if type == 'default':
            log_style = ""
        elif type == 'error':
            log_style = Fore.RED
        elif type == 'success':
            log_style = Fore.GREEN

        now = datetime.now()
        self.logfile = "logs/" + now.strftime("%Y-%m-%d") + ".txt"
        logtime = "[" + now.strftime("%Y-%m-%d %H:%M:%S")+ "]:  "
        logtime_style = (Style.DIM + logtime + Style.RESET_ALL)
        log = (logtime_style + log_style + statement + Style.RESET_ALL)
        print(log)
        self.writeToLog(statement, now)
        pass

    def writeToLog(self, statement, now):
        with open(self.logfile, "a") as f:
            f.write("[" + now.strftime("%Y-%m-%d %H:%M:%S")+ "]:  " + statement + "\n")


if __name__ == "__main__":
    li = Logger()
    li.log("Hello World")
    li.log("Hello World Error", type='error')
    li.log("Hello World Success", type='success')
