import json

from src import SqlHelper

departureKeys = ['id', 'line', 'direction', 'realTime', 'scheduledTime', 'station']


def getAllDepartures():
    return __queryRunner('SELECT * FROM departure')


def getAllDeparturesByStation(station_id):
    return __queryRunner('SELECT * FROM departure WHERE station = {}'.format(station_id))


def __queryRunner(query):
    sqlHelper = SqlHelper()
    result = sqlHelper.execute(query)
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