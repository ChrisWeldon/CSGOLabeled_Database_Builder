from Exceptions import *
from Logger import Logger
from Scraper import *
from DatabaseInterface import DatabaseInterface
import datetime

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
li = Logger()

#print(getMatchData("https://www.hltv.org/matches/2330535/alternate-attax-vs-tricked-united-masters-league"))
#
#cronned for every 5 minutes or so
#team_lineup = ['695/allu', '4076/Aerial', '7248/xseveN', '9816blah/Aleksib', '11916/sergej']

def main():
    print(li.__class__.__name__)
    li.log("Finished")

if __name__ == "__main__":
    main()
