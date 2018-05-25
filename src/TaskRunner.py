import datetime

import time
import threading

from src import DepartureManager, DataProvider

from src.Helper import RequestHelper, Logger

# It is not always necessary to fetch data every minute
# e.g. in the middle of the night
# So we save the time with the next departure to prevent useless traffic

# Because the taskRunner is set to run every 60 seconds this is
# the smallest possible fetch interval

nextFetchMap = {}

url = 'https://webapi.vvo-online.de/dm'
post_fields = {'limit': 20, 'mot': '[Tram, CityBus]'}


def makeRequest(stop_id, sql_worker):
    post_fields['stopid'] = stop_id

    response = RequestHelper.synchronousApiRequest(url, post_fields)

    nextFetchForStation = DepartureManager.createOrUpdateDepartures(response, stop_id, sql_worker)
    nextFetchMap[stop_id] = nextFetchForStation


# create a new thread for every stop to fetch the data.
def run(sql_worker):
    Logger.createLogEntry('Going to fetch data from {} stops'.format(len(nextFetchMap)))
    # init fetching map
    now = datetime.datetime.now()
    for stop_id in nextFetchMap:
        nextFetchMap[stop_id] = now

    while 1:
        now = datetime.datetime.now()
        for stop_id, nextCheck in nextFetchMap.items():
            if nextCheck <= now:
                thread = threading.Thread(target=makeRequest, args=[stop_id, sql_worker])
                thread.start()
        DataProvider.setLastRunToNow()
        time.sleep(60)
