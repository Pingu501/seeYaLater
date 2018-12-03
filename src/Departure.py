import datetime


class Departure:

    def __init__(self, json: dict, stop_id):
        self.id = json['Id']
        self.line = json['LineName']
        self.direction = json['Direction']
        self.scheduledTime = parseDateStringToDate(json['ScheduledTime'])

        # sometimes there is no real time provided
        # we assume that it equals scheduled time
        if 'RealTime' in json.keys():
            self.realTime = parseDateStringToDate(json['RealTime'])
        else:
            self.realTime = parseDateStringToDate(json['ScheduledTime'])

        self.stop_id = stop_id

    def getDelay(self):
        print('{} to {} is to late by {}'.format(self.line, self.direction, self.realTime - self.scheduledTime))


def parseDateStringToDate(date_string: str):
    # TODO: time zoneing!
    prepared_string = date_string.replace('/Date(', '').replace('+0100)/', '').replace('+0200)/', '').replace('-0000)/',
                                                                                                              '')
    return datetime.datetime.fromtimestamp(int(prepared_string) / 1000)
