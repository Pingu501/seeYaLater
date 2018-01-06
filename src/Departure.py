import datetime
import sqlite3


class Departure:

    def __init__(self, json):
        self.id = json['Id']
        self.line = json['LineName']
        self.direction = json['Direction']
        self.realTime = parseDateStringToDate(json['RealTime'])
        self.scheduledTime = parseDateStringToDate(json['ScheduledTime'])

    def getDelay(self):
        print('{} to {} is to late by {}'.format(self.line, self.direction, self.realTime - self.scheduledTime))


def parseDateStringToDate(date_string: str):
    prepared_string = date_string.replace('/Date(', '').replace('+0100)/', '')
    return datetime.datetime.fromtimestamp(int(prepared_string) / 1000)


class DepartureManager:

    def __init__(self):
        self.departures = {}
        self.__prepareDatabase()

    def __prepareDatabase(self):
        self.sql_connection = sqlite3.connect('seeYaLater.db')
        self.__runSQLCommand("""
            CREATE TABLE IF NOT EXISTS departure (
            id INT NOT NULL PRIMARY KEY,
            line VARCHAR(4),
            direction VARCHAR(42),
            realTime DATETIME,
            scheduledTime DATETIME
            )
            
        """)

    def __runSQLCommand(self, sql_command):
        cursor = self.sql_connection.cursor()
        cursor.execute(sql_command)
        self.sql_connection.commit()

    def createOrUpdateDepartures(self, json):
        for departureJson in json['Departures']:
            departure = Departure(departureJson)

            if departure.id in self.departures:
                self.__persistDepartureUpdate(departure)
            else:
                self.__persistDepartureCreation(departure)

            self.departures[departure.id] = departure

    def __persistDepartureCreation(self, departure: Departure):
        command = """
            INSERT INTO departure (id, line, direction, realTime, scheduledTime)
            VALUES ({}, '{}', '{}', '{}', '{}')
        """.format(departure.id, departure.line, departure.direction, departure.realTime,
                   departure.scheduledTime)

        self.__runSQLCommand(command)

    def __persistDepartureUpdate(self, departure: Departure):
        self.__runSQLCommand("""
                    UPDATE departure SET scheduledTime = '{}' WHERE id = {}
                """.format(departure.scheduledTime, departure.id))
