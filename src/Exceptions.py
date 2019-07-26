import traceback
import sys
from Logger import Logger

li = Logger()

class Error(Exception):
    """Base Error Class"""
    pass

class PlayerDataUnscrapableException(Error):
    """Throw this when the scraper screws up somehow. Usually when the data is non existant"""
    def __init__(self, error, name=None):
        if not name:
            self.name = type(self).__name__
        else:
            self.name = name
        li.__init__(self.name)
        li.log(str(type(self).__name__) + ":  "+ str(error), type='error')
    pass

class MatchDataUnscrapableException(Error):
    """Throw when individual match data is unscrapeable"""
    def __init__(self, error, name=None):
        if not name:
            self.name = type(self).__name__
        else:
            self.name = name
        li.__init__(self.name)
        li.log(str(type(self).__name__) + ":  "+ str(error), type='error')
    pass

class MatchesListDataUnscrapableException(Error):
    """Throw when maches list data is unscrapeable"""
    def __init__(self, error, name=None):
        if not name:
            self.name = type(self).__name__
        else:
            self.name = name
        li.__init__(self.name)
        li.log(str(type(self).__name__) + ":  "+ str(error), type='error')
    pass

class LineupIncompleteException(Error):
    """Throw this error when the lineup is not complete,
    EI: not all the players were scrapable. You cant run models on 9 players."""
    def __init__(self, error, name=None):
        if not name:
            self.name = type(self).__name__
        else:
            self.name = name
        li.__init__(self.name)
        li.log(str(type(self).__name__) + ":  "+ str(error), type='error')
    pass

class WriteGroupException(Error):
    def __init__(self, error, name=None):
        if not name:
            self.name = type(self).__name__
        else:
            self.name = name
        li.__init__(self.name)
        li.log(str(type(self).__name__) + ":  "+ str(error), type='error')
    pass

class WriteMatchException(Error):
    def __init__(self, error, name=None):
        if not name:
            self.name = type(self).__name__
        else:
            self.name = name
        li.__init__(self.name)
        li.log(str(type(self).__name__) + ":  "+ str(error), type='error')
    pass

class WritePlayerException(Error):
    def __init__(self, error, name=None):
        if not name:
            self.name = type(self).__name__
        else:
            self.name = name
        li.__init__(self.name)
        li.log(str(type(self).__name__) + ":  "+ str(error), type='error')
    pass

class DatabaseInterfaceCommitException(Error):
    """Throw this error when a commit fails. If primary key already exists"""
    def __init__(self, error, name=None):
        if not name:
            self.name = type(self).__name__
        else:
            self.name = name
        li.__init__(self.name)
        li.log(str(type(self).__name__) + ":  "+ str(error), type='error')
    pass

if __name__ == "__main__":
    try:
        raise PlayerDataUnscrapableException("Blah", name=__name__)
    except Exception as err:
        li.log(traceback.format_exc(), type='traceback')
        li.log("Done", type='success')
