import time
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime

from miner.execution.stop_initializer import StopInitializer
from miner.models import Stop


class Conductor:
    # TODO: type this dict
    wait_times = {}
    executor = ThreadPoolExecutor(max_workers=11)

    departure_url = 'https://webapi.vvo-online.de/dm'
    departure_request_post_fields = {'limit': 10, 'mot': '[Tram, CityBus]'}

    @staticmethod
    def prepare(with_coordinates=False):
        initializer = StopInitializer()

        # first we need to fetch all lines from the stops we already know
        # print('Fetching all lines ...')
        # initializer.fetch_lines_from_initial_stops()

        # then we search for all stops the found line serves
        # print('Fetching all stops from lines ...')
        # initializer.fetch_stops_from_lines()

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
            now = datetime.now().second
            for stop_id in self.wait_times:
                if self.wait_times[stop_id] <= now:
                    self.executor.submit(self.__fetch_departure__(stop_id))
            time.sleep(60)

    def __fetch_departure__(self, stop_id: str):
        print('fetching stop with id {}'.format(stop_id))
        pass
