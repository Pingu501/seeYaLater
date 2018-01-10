from urllib.parse import urlencode
from urllib.request import Request, urlopen
import time
import datetime

import json

from src import DepartureManager

departureManager = DepartureManager()

stop_ids = [33000028, 33000115]

while True:
    for stop_id in stop_ids:
        url = 'https://webapi.vvo-online.de/dm'
        post_fields = {'stopid': stop_id, 'limit': 10, 'mot': '[Tram, CityBus]'}

        request = Request(url, urlencode(post_fields).encode())

        response = urlopen(request).read().decode()
        parsedResponse = json.loads(response)
        departureManager.createOrUpdateDepartures(parsedResponse, stop_id)

    print("{}: fetched {} stations".format(datetime.datetime.now(), len(stop_ids)))
    time.sleep(60)
