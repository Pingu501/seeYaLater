import time
from concurrent.futures.thread import ThreadPoolExecutor
import datetime

import re
import requests

from miner.execution.stop_initializer import StopInitializer
from miner.models import Stop, Departure, Line


class Conductor:
    # TODO: type this dict
    wait_times = {}
    executor = ThreadPoolExecutor(max_workers=11)

    @staticmethod
    def prepare(with_coordinates=False):
        initializer = StopInitializer()

        # first we need to fetch all lines from the stops we already know
        print('Fetching all lines ...')
        initializer.fetch_lines_from_initial_stops()

        # then we search for all stops the found line serves
        print('Fetching all stops from lines ...')
        initializer.fetch_stops_from_lines()

        # get the coordinates of the stops
        if with_coordinates:
            print('Fetching coordinates of stops ...')
            initializer.fetch_stop_coordinates()

    def start(self):
        self.__init_wait_times__()
        self.executor.submit(self.__start_scheduler__())

    def __init_wait_times__(self):
        self.wait_times = {stop.id: 0 for stop in Stop.objects.all()}

    def __start_scheduler__(self):
        while True:
            now = datetime.datetime.now().second
            for stop_id in self.wait_times:
                if self.wait_times[stop_id] <= now:
                    self.executor.submit(self.__fetch_departure__(stop_id))
                time.sleep(60)

    def __fetch_departure__(self, stop_id: str):
        response = requests.get('https://webapi.vvo-online.de/dm',
                                {'limit': 10, 'mot': '[Tram, CityBus]', 'stopid': stop_id})

        if response.status_code >= 400:
            print('Error while fetching departure: {}', response.json())
            return

        stop = Stop.objects.get(id=stop_id)
        for departure_json in response.json()['Departures']:
            self.__create_departure_from_json__(departure_json, stop)

    @staticmethod
    def __create_departure_from_json__(departure_json: dict, stop: Stop):
        try:
            line = Line.objects.get(name=departure_json['LineName'], direction=departure_json['Direction'])
        except Line.DoesNotExist:
            print('Line number {} to {} does not exists, skipping'.format(departure_json['LineName'],
                                                                          departure_json['Direction']))
            return None

        departure = Departure.objects.get_or_create(stop=stop, internal_id=departure_json['Id'], line=line)[0]

        departure.scheduled_time = Conductor.__parse_date_string_to_datetime(departure_json['ScheduledTime'])
        departure.real_time = Conductor.__parse_date_string_to_datetime(
            departure_json['RealTime' if 'RealTime' in departure_json.keys() else 'ScheduledTime'])

        departure.save()

    @staticmethod
    def __parse_date_string_to_datetime(date: str) -> datetime:
        p = re.match(r"/Date\((\d{13})([-|+]0\d)00\)/", date)

        timestamp = int(p.group(1))
        timedelta = datetime.timedelta(hours=int(p.group(2)))

        return datetime.datetime.fromtimestamp(timestamp / 1000, datetime.timezone(timedelta))
