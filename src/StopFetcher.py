from datetime import datetime

import sys
import time

from src import TaskRunner
from src.Helper import RequestHelper

url_departures = 'https://webapi.vvo-online.de/dm'
url_trip = 'https://webapi.vvo-online.de/dm/trip'

initial_known_stops = [33000005, 33000007, 33000028, 33000115, 33000727, 33000052, 33000111, 33000742]

known_lines = {}


def initStops():
    if sys.argv.count('--all'):
        __fetchAllLinesFromAllStop__()
        __fetchAllStopsFromAllLines__()
    else:
        __addStopArrayToFetchList__(initial_known_stops)


def __fetchAllLinesFromAllStop__():
    for stop_id in initial_known_stops:
        response = RequestHelper.synchronousApiRequest(url_departures, {'stopid': stop_id, 'mot': '[Tram, CityBus]', 'limit': 10})

        for departure in response['Departures']:
            known_lines[departure['LineName']] = {'tripId': int(departure['Id']), 'stopId': int(stop_id)}


def __fetchAllStopsFromAllLines__():
    for line in known_lines:
        line_ids = known_lines[line]
        __fetchStopsFromLine__(line_ids['tripId'], line_ids['stopId'])


def __fetchStopsFromLine__(trip_id, stop_id):
    timeString = '/Date({}000+0100)/'.format(round(time.time()))
    post_fields = {'tripId': trip_id, 'stopId': 33000007, 'time': timeString}

    response = RequestHelper.synchronousApiRequest(url_trip, post_fields)

    stopIds = []
    for stop in response['Stops']:
        stopIds.append(stop['Id'])

    __addStopArrayToFetchList__(stopIds)


def __addStopArrayToFetchList__(stop_array):
    now = datetime.now()
    for stop in stop_array:
        TaskRunner.nextFetchMap[int(stop)] = now
