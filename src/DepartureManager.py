import datetime
import logging

from src import Departure
from src.SqlWorker import SqlWorker


logger = logging.getLogger()

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


def createOrUpdateDepartures(json, stop_id, sql_worker):
    """

    :param json: string
    :param stop_id: string
    :type sql_worker: SqlWorker
    """
    # add 1 day to now as default value
    nearestDeparture = datetime.datetime.now() + datetime.timedelta(1)

    for departureJson in json['Departures']:

        if not __isValidDepartureJson(departureJson):
            logger.log(logging.WARNING, 'JSON: {} \n is not valid'.format(departureJson))
            continue

        departure = Departure(departureJson, stop_id)

        if departure.realTime < nearestDeparture:
            nearestDeparture = departure.realTime

        sql_worker.onThread(sql_worker.createOrUpdate, [departure])

    return nearestDeparture
