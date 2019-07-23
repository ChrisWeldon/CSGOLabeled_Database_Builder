import traceback
import sys
from src.Logger import Logger

li = Logger()

class Error(Exception):
    """Base Error Class"""
    pass

class PlayerDataUnscrapableException(Error):
    """Throw this when the scraper screws up somehow. Usually when the data is non existant"""
    def __init__(self, error):
        li.log(str(type(self).__name__) + ":  "+ str(error), type='error')
    pass

class MatchDataUnscrapableException(Error):
    """Throw when individual match data is unscrapeable"""
    def __init__(self, error):
        li.log(str(type(self).__name__) + ":  "+ str(error), type='error')
    pass

class MatchesListDataUnscrapableException(Error):
    """Throw when maches list data is unscrapeable"""
    def __init__(self, error):
        li.log(str(type(self).__name__) + ":  "+ str(error), type='error')
    pass

class LineupIncompleteException(Error):
    """Throw this error when the lineup is not complete,
    EI: not all the players were scrapable. You cant run models on 9 players."""
    def __init__(self, error):
        li.log(str(type(self).__name__) + ":  "+ str(error), type='error')
    pass

class WriteGroupException(Error):
    def __init__(self, error):
        li.log(str(type(self).__name__) + ":  "+ str(error), type='error')
    pass

class WriteMatchException(Error):
    def __init__(self, error):
        li.log(str(type(self).__name__) + ":  "+ str(error), type='error')
    pass

class WritePlayerException(Error):
    def __init__(self, error):
        li.log(str(type(self).__name__) + ":  "+ str(error), type='error')
    pass

class DatabaseInterfaceCommitException(Error):
    """Throw this error when a commit fails. If primary key already exists"""
    def __init__(self, error):
        li.log(str(type(self).__name__) + ":  "+ str(error), type='error')
    pass
