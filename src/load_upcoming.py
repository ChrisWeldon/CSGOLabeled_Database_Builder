from DatabaseInterface import DatabaseInterface
import datetime, time, sched, sys
from Exceptions import *
from Scraper import *
from Logger import Logger
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

#li.log(getMatchData("https://www.hltv.org/matches/2330535/alternate-attax-vs-tricked-united-masters-league"))
#
#cronned for every 5 minutes or so
#team_lineup = ['695/allu', '4076/Aerial', '7248/xseveN', '9816blah/Aleksib', '11916/sergej']

schedule_time = 30
s = sched.scheduler(time.time, time.sleep)
li = Logger(name="main_upcm", caller="load_upcomingpy")
di = DatabaseInterface()

def load_upcoming():
    try:
        up_matches  = getUpcomingMatches(20)
        for m in up_matches:
            match_id = m[0]
            start_time = m[1]
            if(not di.checkUpcomingMatchInDatabase(match_id)):
                #li.log(match_id.split('/')[2] + " available", type="success") # weird that the except warrants success. That's fine though
                try:
                    di.writeMatch(match_id)
                except LineupIncompleteException as err:
                    #li.log(traceback.format_exc(), type='traceback')
                    pass
                except WriteMatchException as err:
                    li.log(traceback.format_exc(), type='traceback')
                    pass
            else:
                li.log("already collected " + match_id)
    except Exception as err:
        li.log(traceback.format_exc(), type='traceback')
        li.log(type(err).__name__, type='error')
    s.enter(schedule_time, 1, load_upcoming)

if __name__ == "__main__":
    li.log("Feature Collection Started")
    s.enter(1, 1, load_upcoming)
    s.run()
