from datetime import datetime, timezone

import sys

from src import TaskRunner
from src.Helper import RequestHelper, Logger

url_departures = 'https://webapi.vvo-online.de/dm'
url_trip = 'https://webapi.vvo-online.de/dm/trip'

initial_known_stops = [33000005, 33000007, 33000028, 33000115, 33000727, 33000052, 33000111, 33000742]

known_lines = {}


def initStops():
    if sys.argv.count('--all'):
        Logger.createLogEntry('Start fetching all stops')
        __fetchAllLinesFromAllStop__()
        __fetchAllStopsFromAllLines__()
    else:
        Logger.createLogEntry('Add {} initial stops to fetch list'.format(len(initial_known_stops)))
        __addStopArrayToFetchList__(initial_known_stops)


def __fetchAllLinesFromAllStop__():
    for stop_id in initial_known_stops:
        response = RequestHelper.synchronousApiRequest(url_departures,
                                                       {'stopid': stop_id, 'mot': '[Tram, CityBus]', 'limit': 20})

        for departure in response['Departures']:
            known_lines[departure['LineName']] = {'tripId': int(departure['Id']), 'stopId': int(stop_id)}


def __fetchAllStopsFromAllLines__():
    for line in known_lines:
        line_ids = known_lines[line]
        __fetchStopsFromLine__(line_ids['tripId'], line_ids['stopId'])


def __fetchStopsFromLine__(trip_id, stop_id):
    utc_dt = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    post_fields = {'tripId': trip_id, 'stopId': stop_id, 'time': utc_dt}

    response = RequestHelper.synchronousApiRequest(url_trip, post_fields)

    if not response:
        return

    stopIds = []
    for stop in response['Stops']:
        stopIds.append(stop['Id'])

    __addStopArrayToFetchList__(stopIds)


def __addStopArrayToFetchList__(stop_array):
    now = datetime.now()
    for stop in stop_array:
        TaskRunner.nextFetchMap[int(stop)] = now
