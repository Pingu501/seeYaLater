import datetime

import time
import threading

from src import DepartureManager, DataProvider, StopFetcher

from src.Helper import RequestHelper, Logger

# It is not always necessary to fetch data every minute
# e.g. in the middle of the night
# So we save the time with the next departure to prevent useless traffic

# Because the taskRunner is set to run every 60 seconds this is
# the smallest possible fetch interval

fetchMap = {}

url = 'https://webapi.vvo-online.de/dm'
post_fields = {'limit': 10, 'mot': '[Tram, CityBus]'}


def makeRequest(stop_id, sql_worker):
    post_fields['stopid'] = stop_id
    response = RequestHelper.synchronousApiRequest(url, post_fields)

    return DepartureManager.createOrUpdateDepartures(response, stop_id, sql_worker)


def lineFetcher(line_id, sql_worker):
    stops = StopFetcher.known_lines_with_stops[line_id]['stops']
    # add 1 day to know to make sure this gets overwritten
    next_fetch = datetime.datetime.now() + datetime.timedelta(1)
    while 1:
        for stop_id in stops:
            if stops[stop_id] <= datetime.datetime.now():
                next_fetch_time_stop = makeRequest(stop_id, sql_worker)
                StopFetcher.known_lines_with_stops[line_id]['stops'][stop_id] = next_fetch_time_stop

                if next_fetch_time_stop < next_fetch:
                    next_fetch = next_fetch_time_stop

        sleep_time = (datetime.datetime.now() - next_fetch).total_seconds()

        # wait at least one minute
        if sleep_time < 60:
            sleep_time = 60
        # wait not longer then one hour
        if sleep_time > 60 * 60:
            sleep_time = 60 * 60

        Logger.createLogEntry('Line {} finished fetching \n going to sleep for {} seconds'.format(line_id, sleep_time))
        time.sleep(sleep_time)


# create a new thread for every line which fetches all stops
def run(sql_worker):
    Logger.createLogEntry(
        'Going to fetch data from {} lines containing {} stops'.format(len(StopFetcher.known_lines_with_stops),
                                                                       len(StopFetcher.known_stops)))
    for line_id in StopFetcher.known_lines_with_stops:
        line = StopFetcher.known_lines_with_stops[line_id]
        if len(line['stops']) > 0:
            thread = threading.Thread(target=lineFetcher, args=[line_id, sql_worker])
            thread.start()
