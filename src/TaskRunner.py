from urllib.parse import urlencode
from urllib.request import Request, urlopen

import time
import json
import threading

from src import DepartureManager, Logger, DataProvider

stop_ids = [33000005, 33000007, 33000028, 33000115, 33000727]

url = 'https://webapi.vvo-online.de/dm'
post_fields = {'limit': 10, 'mot': '[Tram, CityBus]'}


def makeRequest(stop_id):
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


# create a new thread for every stop to fetch the data.
def run():
    while 1:
        for stop_id in stop_ids:
            thread = threading.Thread(target=makeRequest, args=[stop_id])
            thread.start()
        print(threading.active_count())
        time.sleep(60)
