from datetime import datetime
from colorama import Fore, Back, Style
import inspect, json

class Logger:
    def __init__(self, name=None, dir_rel='../logs/'):
        with open('./config.json', 'r') as json_file:
            text = json_file.read()
            json_data = json.loads(text)
            self.config = json_data
        self.dir_rel = dir_rel
        self.name = name
        self.logfile = "dateless.txt"
        if self.name:
            self.logname_w_style = (Style.DIM + "(" + self.name + ") " + Style.RESET_ALL + "\t")
        else:
            self.logname_w_style = ""

    def dump_meta(self, meta):
        if self.config["dev"] != "True":
            with open("/usr/bin/CSGOLabeled_Database_Builder/logs/metadata.json", "w") as f:
                json.dump(meta, f)
        else:
            with open(self.dir_rel + "metadata.json", "w") as f:
                json.dump(meta, f)
        pass
    def log(self, statement, type='default', style='default'):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        caller = calframe[-1][1].split('/')[-1]
        log_style = ""
        if type == 'default':
            log_style = ""
        elif type == 'error':
            log_style = Fore.RED
        elif type == 'success':
            log_style = Fore.GREEN
        elif type == 'traceback':
            log_style = '\033[91m' #Light Red
        elif type == 'attempt':
            log_style = '\033[33m'#Orange


        now = datetime.now()
        self.logfile = now.strftime("%Y-%m-%d") + "-" + caller + ".log"
        logtime = "[" + now.strftime("%Y-%m-%d %H:%M:%S")+ "]"
        logtime_w_style = (Style.DIM + logtime + "["+caller+"]" +":  " + Style.RESET_ALL)
        log_print = (logtime_w_style + self.logname_w_style + log_style + statement + Style.RESET_ALL)
        print(log_print)
        self.writeToLog(statement, now=now)
        pass

    def loglist(self, list, type='default', style='default'):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        caller = calframe[-1][1].split('/')[-1]

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
        self.logfile = now.strftime("%Y-%m-%d") + "-" + caller + ".log"
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
        if self.config["dev"] != "True":
            with open("/usr/bin/CSGOLabeled_Database_Builder/logs/" + str(self.logfile), "a") as f:
                if now:
                    f.write("[" + now.strftime("%Y-%m-%d %H:%M:%S")+ "]:  (" + self.name +") " + statement + "\n")
                else:
                    f.write("\t" + statement + "\n")
        else:
            with open(self.dir_rel + self.logfile, "a") as f:
                if now:
                    f.write("[" + now.strftime("%Y-%m-%d %H:%M:%S")+ "]:  (" + self.name +") " + statement + "\n")
                else:
                    f.write("\t" + statement + "\n")

if __name__ == "__main__":
    li = Logger()
    li.log("Hello World")
    li.log("Hello World Error", type='error')
    li.log("Hello World Success", type='success')
