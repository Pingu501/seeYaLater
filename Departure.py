import datetime


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

    def createOrUpdateDepartures(self, json):
        for departureJson in json["Departures"]:
            departure = Departure(departureJson)

            if departure.id in self.departures:
                print('update')
            else:
                print('create')

            self.departures[departure.id] = departure
