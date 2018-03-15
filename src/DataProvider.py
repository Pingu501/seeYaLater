from datetime import datetime
import json

from src.Helper import SqlHelper

departureKeys = ['id', 'line', 'direction', 'realTime', 'scheduledTime', 'station']
lastRun = datetime.now()


def setLastRunToNow():
    global lastRun
    lastRun = datetime.now()


def getCurrentStatus():
    numberOfEntries = SqlHelper.count('departure')
    return '{"totalCount": ' + str(numberOfEntries) + ', "lastRun": ' + str(lastRun) + '}'


def getAllDepartures():
    return __jsonCreator(SqlHelper.select('departure', '*', []), departureKeys)


def getAllDeparturesByStation(station_id):
    return __jsonCreator(SqlHelper.select('departure', '*', [['station', '=', station_id]]), departureKeys)


def __queryRunner(query):
    result = SqlHelper.execute(query)
    return __jsonCreator(result, departureKeys)


def __jsonCreator(sql_result, keys):
    dictResult = []
    rowNumber = 0
    for entry in sql_result:
        index = 0
        keyValuePairs = {}
        for value in entry:
            keyValuePairs[keys[index]] = value
            index += 1
        dictResult.append(keyValuePairs)
        rowNumber += 1

    return json.dumps(dictResult)
