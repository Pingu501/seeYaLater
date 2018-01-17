from urllib.parse import urlencode
from urllib.request import Request, urlopen

import time
import json

from src import DepartureManager, SqlHelper, Logger


stop_ids = [33000028, 33000115]


def fetchStation(station_id, departure_manager):
    url = 'https://webapi.vvo-online.de/dm'
    post_fields = {'stopid': station_id, 'limit': 10, 'mot': '[Tram, CityBus]'}

    request = Request(url, urlencode(post_fields).encode())

    try:
        response = urlopen(request).read().decode()
    except:
        Logger.createLogEntry("could not connect to the API")
        return

    parsed_response = json.loads(response)
    departure_manager.createOrUpdateDepartures(parsed_response, station_id)


def run():
    sqlHelper = SqlHelper()
    departure_manager = DepartureManager(sqlHelper)
    print("starting task runner")
    while True:
        for station_id in stop_ids:
            fetchStation(station_id, departure_manager)

        time.sleep(60)
