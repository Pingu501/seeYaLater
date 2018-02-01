from urllib.parse import urlencode
from urllib.request import Request, urlopen
from threading import Thread

import time
import json

from src import DepartureManager, Logger, DataProvider

stop_ids = [33000005, 33000007, 33000028, 33000115, 33000727]

url = 'https://webapi.vvo-online.de/dm'
post_fields = {'limit': 10, 'mot': '[Tram, CityBus]'}


def makeRequest(stop_id):
    while True:
        post_fields['stopid'] = stop_id
        request = Request(url, urlencode(post_fields).encode())

        try:
            response = urlopen(request).read().decode()
        except Exception:
            Logger.createLogEntry("could not connect to the API")
            return

        parsed_response = json.loads(response)
        DepartureManager.createOrUpdateDepartures(parsed_response, stop_id)

        DataProvider.setLastRunToNow()
        time.sleep(60)


# create a new thread for every stop to fetch the data.
def run():
    for stop_id in stop_ids:
        thread = Thread(target=makeRequest, args=[stop_id])
        thread.start()
