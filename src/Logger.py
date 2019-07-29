from datetime import datetime
from colorama import Fore, Back, Style

class Logger:
    def __init__(self, name=None, dir_rel='../logs/'):
        self.dir_rel = dir_rel
        self.name = name
        self.logfile = "dateless.txt"
        if name:
            self.logname_w_style = (Style.DIM + "(" + self.name + ") " + Style.RESET_ALL + "\t")
        else:
            self.logname_w_style = ""

    def log(self, statement, type='default', style='default'):
        log_style = ""
        if type == 'default':
            log_style = ""
        elif type == 'error':
            log_style = Fore.RED
        elif type == 'success':
            log_style = Fore.GREEN
        elif type == 'traceback':
            log_style = '\033[91m' #Light Red


        now = datetime.now()
        self.logfile = self.dir_rel+ now.strftime("%Y-%m-%d") + ".log"
        logtime = "[" + now.strftime("%Y-%m-%d %H:%M:%S")+ "]:  "
        logtime_w_style = (Style.DIM + logtime + Style.RESET_ALL)
        log = (logtime_w_style + self.logname_w_style + log_style + statement + Style.RESET_ALL)
        print(log)
        self.writeToLog(statement, now=now)
        pass

    def loglist(self, list, type='default', style='default'):
        if type == 'default':
            log_style = ""
        elif type == 'error':
            log_style = Fore.RED
        elif type == 'success':
            log_style = Fore.GREEN
        elif type == 'traceback':
            log_style = '\033[91m' #Light Red
        elif type == 'attempt':
            log_Style = '\033[33m' #Orange


        now = datetime.now()
        self.logfile = self.dir_rel+ now.strftime("%Y-%m-%d") + ".log"
        logtime = "[" + now.strftime("%Y-%m-%d %H:%M:%S")+ "]:  "
        logtime_w_style = (Style.DIM + logtime + Style.RESET_ALL)
        log = (logtime_w_style + self.logname_w_style + log_style + "<List>"+ Style.RESET_ALL)
        print(log)
        self.writeToLog("<List>:", now)
        for i in list:
            print("\t\t - " + log_style + str(i) + Style.RESET_ALL)
            self.writeToLog(str(i), now = now)
        pass

    def writeToLog(self, statement, now=None):
        with open(self.logfile, "a") as f:
            if now:
                f.write("[" + now.strftime("%Y-%m-%d %H:%M:%S")+ "]:  " + self.logname_w_style + statement + "\n")
            else:
                f.write("\t" + statement + "\n")

if __name__ == "__main__":
    li = Logger()
    li.log("Hello World")
    li.log("Hello World Error", type='error')
    li.log("Hello World Success", type='success')
