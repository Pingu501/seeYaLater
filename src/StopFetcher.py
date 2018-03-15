import time

from src import TaskRunner
from src.Helper import RequestHelper

url = "https://webapi.vvo-online.de/dm/trip"


def fetchAllStopsFromLine():
    timeString = '/Date({}000+0100)/'.format(round(time.time()))
    post_fields = {'tripId': 73363595, 'stopId': 33000007, 'time': timeString}

    response = RequestHelper.synchronousApiRequest(url, post_fields)

    for stop in response['Stops']:
        TaskRunner.known_stops.append(stop['Id'])
