from datetime import datetime


def createLogEntry(log: str):
    with open('history.log', 'a+') as log_file:
        log_file.write('{}: {}{}'.format(datetime.now(), log, '\n'))
