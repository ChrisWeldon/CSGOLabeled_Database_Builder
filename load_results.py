from src.Exceptions import PlayerDataUnscrapableException
from src.Exceptions import MatchDataUnscrapableException
from src.Exceptions import MatchesListDataUnscrapableException
from DatabaseInterface import DatabaseInterface
import datetime, time, sched
from src.Exceptions import *
from Scraper import *
import sys
"""


MAIN SCRIPT:
All primary functionality should be placed below

MTID (Match-Time Identification)   One per game that occurs. Represents a match with its data.
PMID (Player-Time Identification) Ten per game that occurs. Represents player data with time sensitive variables.
GPMID (Group Player Match Identification) two per game that occurer. Represents teams.


Match type:
    best of 1 : 0
    best of 2 : 1
    best of 3 : 2
    best of 5 : 3
    best of 1 (LAN): 4
    best of 2 (LAN): 5
    best of 3 (LAN): 6
    best of 5 (LAN): 7

"""

#print(getMatchData("https://www.hltv.org/matches/2330535/alternate-attax-vs-tricked-united-masters-league"))
#
#cronned for every 5 minutes or so
#team_lineup = ['695/allu', '4076/Aerial', '7248/xseveN', '9816blah/Aleksib', '11916/sergej']

schedule_time = 10
s = sched.scheduler(time.time, time.sleep)

def load_results():
    print("checking for results")
    di = DatabaseInterface()
    di.checkWriteResults()
    print("Finished")
    del di
    sys.stdout.flush()
    s.enter(schedule_time, 1, load_results)

if __name__ == "__main__":

    s.enter(schedule_time, 1, load_results)
    s.run()
