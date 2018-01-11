import sqlite3

from src import Departure
from src import Logger


class DepartureManager:

    def __init__(self):
        self.__prepareDatabase()

    def __prepareDatabase(self):
        self.sql_connection = sqlite3.connect('seeYaLater.db')
        self.__runSQLCommand("""
            CREATE TABLE IF NOT EXISTS departure (
            id INT NOT NULL PRIMARY KEY,
            line VARCHAR(4),
            direction VARCHAR(42),
            realTime DATETIME,
            scheduledTime DATETIME,
            station INT
            )

        """)

    def __runSQLCommand(self, sql_command):
        cursor = self.sql_connection.cursor()
        cursor.execute(sql_command)
        self.sql_connection.commit()
        return cursor.fetchone()

    def createOrUpdateDepartures(self, json, stop_id):
        for departureJson in json['Departures']:

            if not isValidDepartureJson(departureJson):
                print('JSON: {} \n is not valid'.format(departureJson))
                continue

            departure = Departure(departureJson, stop_id)
            result = self.__runSQLCommand('SELECT COUNT(id) FROM departure WHERE id = ' + departure.id)

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

        self.__runSQLCommand(command)

    def __persistDepartureUpdate(self, departure: Departure):
        self.__runSQLCommand("""
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
