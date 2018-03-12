import datetime
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import time
import json
import threading

from src import DepartureManager, Logger, DataProvider

stop_ids = [33000005, 33000007, 33000028, 33000115, 33000727]


# It is not always necessary to fetch data every minute
# e.g. in the middle of the night
# So we save the time with the next departure to prevent useless traffic

# Because the taskRunner is set to run every 60 seconds this is
# the smallest possible fetch interval
nextFetchMap = {}

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
    nextFetchForStation = DepartureManager.createOrUpdateDepartures(parsed_response, stop_id)
    nextFetchMap[stop_id] = nextFetchForStation

    DataProvider.setLastRunToNow()


# create a new thread for every stop to fetch the data.
def run():
    # init fetching map
    now = datetime.datetime.now()
    for stop_id in stop_ids:
        nextFetchMap[stop_id] = now

    while 1:
        now = datetime.datetime.now()
        for stop_id, nextCheck in nextFetchMap.items():
            if nextCheck <= now:
                thread = threading.Thread(target=makeRequest, args=[stop_id])
                thread.start()
        time.sleep(60)
