import datetime

from src import Departure, Logger, SqlHelper


def makeString(arg):
    return "'" + str(arg) + "'"


def __isValidDepartureJson(departure_json):
    is_valid = True
    fields = ['Id', 'LineName', 'Direction', 'RealTime', 'ScheduledTime']

    for field in fields:
        try:
            departure_json[field]
        except KeyError:
            if not field == "RealTime":
                is_valid = False
            pass

    return is_valid


def createOrUpdateDepartures(json, stop_id):
    # add 1 day to now as default value
    nearestDeparture = datetime.datetime.now() + datetime.timedelta(1)

    for departureJson in json['Departures']:

        if not __isValidDepartureJson(departureJson):
            Logger.createLogEntry('JSON: {} \n is not valid'.format(departureJson))
            continue

        departure = Departure(departureJson, stop_id)

        if departure.realTime < nearestDeparture:
            nearestDeparture = departure.realTime

        result = SqlHelper.execute('SELECT COUNT(id) FROM departure WHERE id = ' + departure.id)

        if result[0][0] == 0:
            SqlHelper.create("departure",
                             ["id", "line", "direction", "realTime", "scheduledTime", "station"],
                             [departure.id, makeString(departure.line), makeString(departure.direction),
                              makeString(departure.realTime), makeString(departure.scheduledTime),
                              makeString(departure.stop_id)])
        else:
            SqlHelper.update("departure",
                             {'scheduledTime': makeString(departure.scheduledTime)},
                             "id = {}".format(departure.id))

    Logger.createLogEntry("fetched station with id {}".format(stop_id))
    return nearestDeparture
