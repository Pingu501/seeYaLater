from datetime import datetime, timezone

import sys
import logging

from src.Helper import RequestHelper

logger = logging.getLogger()

url_departures = 'https://webapi.vvo-online.de/dm'
url_trip = 'https://webapi.vvo-online.de/dm/trip'

now = datetime.now()
initial_known_stops = [33000005, 33000007, 33000028, 33000115, 33000727, 33000052, 33000111, 33000742]
known_lines_with_stops = {}
known_stops = []


def initStops():
    if sys.argv.count('--all'):
        logger.log(logging.INFO, 'Start fetching all stops')
        __fetchAllLinesFromInitialStops__()
        __fetchAllStopsFromAllLines__()
    else:
        logger.log(logging.INFO, 'Add {} initial stops to fetch list'.format(len(initial_known_stops)))
        __createFetchMapForInitialStops__()


def __createFetchMapForInitialStops__():
    global known_stops
    known_stops = initial_known_stops

    line_zero = {}
    stops = {}
    for stop_id in initial_known_stops:
        stops[stop_id] = now
    line_zero['stops'] = stops
    known_lines_with_stops[0] = line_zero


def __fetchAllLinesFromInitialStops__():
    for stop_id in initial_known_stops:
        response = RequestHelper.synchronousApiRequest(url_departures,
                                                       {'stopid': stop_id, 'mot': '[Tram, CityBus]', 'limit': 20})

        for departure in response['Departures']:
            known_lines_with_stops[departure['LineName']] = {'tripId': int(departure['Id']), 'stopId': int(stop_id)}


def __fetchAllStopsFromAllLines__():
    for line in known_lines_with_stops:
        line_ids = known_lines_with_stops[line]
        stopsOfLine = __fetchStopsFromLine__(line_ids['tripId'], line_ids['stopId'])
        known_lines_with_stops[line]['stops'] = stopsOfLine


def __fetchStopsFromLine__(trip_id, stop_id):
    utc_dt = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    post_fields = {'tripId': trip_id, 'stopId': stop_id, 'time': utc_dt}

    response = RequestHelper.synchronousApiRequest(url_trip, post_fields)

    if not response:
        return

    stopIds = {}
    for stop in response['Stops']:
        stop_id = stop['Id']
        if stop_id not in known_stops:
            stopIds[stop_id] = now
            known_stops.append(stop_id)

    return stopIds
