import datetime


class Departure:

    def __init__(self, json, stop_id):
        self.id = json['Id']
        self.line = json['LineName']
        self.direction = json['Direction']
        self.realTime = parseDateStringToDate(json['RealTime'])
        self.scheduledTime = parseDateStringToDate(json['ScheduledTime'])
        self.stop_id = stop_id

    def getDelay(self):
        print('{} to {} is to late by {}'.format(self.line, self.direction, self.realTime - self.scheduledTime))


def parseDateStringToDate(date_string: str):
    prepared_string = date_string.replace('/Date(', '').replace('+0100)/', '')
    return datetime.datetime.fromtimestamp(int(prepared_string) / 1000)
