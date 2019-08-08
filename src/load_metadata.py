from Exceptions import PlayerDataUnscrapableException
from Exceptions import MatchDataUnscrapableException
from Exceptions import MatchesListDataUnscrapableException
from DatabaseInterface import DatabaseInterface
import datetime, time, sched
from Exceptions import *
from Scraper import *
from Logger import Logger
import sys
import os

schedule_time = 30
s = sched.scheduler(time.time, time.sleep)
li = Logger(name="load_results")
li.log("load_results.py Initialized")

def load_metadata():
    di = DatabaseInterface()
    meta = di.getMetaData()
    meta['orphaned_groups'] = meta['groups_count'] % (meta['matches_complete_count']*2)
    meta['orphaned_players'] = meta['players_count'] % (meta['groups_count']*5)

    li.dump_meta(meta)

    del di
    s.enter(schedule_time, 1, load_metadata)

if __name__ == '__main__':
    li.log("Label collection started")
    s.enter(1, 1, load_metadata)
    s.run()
