from urllib.parse import urlencode
from urllib.request import Request, urlopen
import time

import json

from src import Departure

departureManager = Departure.DepartureManager()

while True:
    url = 'https://webapi.vvo-online.de/dm'
    post_fields = {'stopid': '33000028', 'limit': 10, 'mot': '[Tram, CityBus]'}

    request = Request(url, urlencode(post_fields).encode())

    response = urlopen(request).read().decode()
    parsedResponse = json.loads(response)
    departureManager.createOrUpdateDepartures(parsedResponse)

    time.sleep(60)
