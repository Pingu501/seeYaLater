from datetime import datetime


def createLogEntry(log: str):
    with open('history.log', 'a+') as log_file:
        message = '{}: {}'.format(datetime.now(), log)
        log_file.write(message + '\n')
        print(message)
