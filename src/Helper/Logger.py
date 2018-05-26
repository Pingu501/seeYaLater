from datetime import datetime

import sys


def createLogEntry(log: str):
    message = '{}: {}'.format(datetime.now(), log)
    print(message)


def verbose(log: str):
    if sys.argv.count('-v'):
        createLogEntry(log)
