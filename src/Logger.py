from datetime import datetime


def createLogEntry(log: str):
    message = '{}: {}'.format(datetime.now(), log)
    print(message)