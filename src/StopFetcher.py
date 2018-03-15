from datetime import datetime

import time

from src import TaskRunner
from src.Helper import RequestHelper

url = "https://webapi.vvo-online.de/dm/trip"

initial_known_stops = [33000005, 33000007, 33000028, 33000115, 33000727]


def fetchAllStopsFromLine():
    timeString = '/Date({}000+0100)/'.format(round(time.time()))
    post_fields = {'tripId': 73363595, 'stopId': 33000007, 'time': timeString}

    response = RequestHelper.synchronousApiRequest(url, post_fields)

    stopIds = []
    for stop in response['Stops']:
        stopIds.append(stop['Id'])

    addStopArrayToFetchList(stopIds)


def addStopArrayToFetchList(stop_array):
    now = datetime.now()
    for stop in stop_array:
        TaskRunner.nextFetchMap[int(stop)] = now


addStopArrayToFetchList(initial_known_stops)
