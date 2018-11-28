from datetime import datetime
import json

departureKeys = ['id', 'line', 'direction', 'realTime', 'scheduledTime', 'station']
lastRun = datetime.now()


class DataProvider:
    def __init__(self, sql_worker):
        self.sql_worker = sql_worker

    @staticmethod
    def setLastRunToNow():
        global lastRun
        lastRun = datetime.now()

    def getCurrentStatus(self):
        numberOfEntries = self.sql_worker.count('departure')
        return '{"totalCount": ' + str(numberOfEntries) + ', "lastRun": ' + str(lastRun) + '}'

    def getAllDepartures(self):
        return self.__jsonCreator(self.sql_worker.select('departure', '*', []), departureKeys)


    def getAllDeparturesByStation(self, station_id):
        result = self.sql_worker.select('departure', '*', [['station', '=', station_id]])
        return self.__jsonCreator(result, departureKeys)

    def __queryRunner(self, query):
        result = self.sql_worker.execute(query)
        return self.__jsonCreator(result, departureKeys)

    @staticmethod
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
