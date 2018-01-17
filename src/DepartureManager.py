from src import Departure
from src import Logger


class DepartureManager:

    def __init__(self, sqlHelper):
        self.sql_helper = sqlHelper

    def createOrUpdateDepartures(self, json, stop_id):
        for departureJson in json['Departures']:

            if not isValidDepartureJson(departureJson):
                Logger.createLogEntry('JSON: {} \n is not valid'.format(departureJson))
                continue

            departure = Departure(departureJson, stop_id)
            result = self.sql_helper.execute('SELECT COUNT(id) FROM departure WHERE id = ' + departure.id)

            if result[0]:
                self.__persistDepartureUpdate(departure)
            else:
                self.__persistDepartureCreation(departure)

        Logger.createLogEntry("fetched station with id {}".format(stop_id))

    def __persistDepartureCreation(self, departure: Departure):
        command = """
            INSERT INTO departure (id, line, direction, realTime, scheduledTime, station)
            VALUES ({}, '{}', '{}', '{}', '{}', {})
        """.format(departure.id, departure.line, departure.direction, departure.realTime,
                   departure.scheduledTime, departure.stop_id)

        self.sql_helper.execute(command)

    def __persistDepartureUpdate(self, departure: Departure):
        self.sql_helper.execute("""
                    UPDATE departure SET scheduledTime = '{}' WHERE id = {}
                """.format(departure.scheduledTime, departure.id))


def isValidDepartureJson(departure_json):
    is_valid = True
    fields = ['Id', 'LineName', 'Direction', 'RealTime', 'ScheduledTime']

    for field in fields:
        try:
            departure_json[field]
        except KeyError:
            is_valid = False
            pass

    return is_valid
