from multiprocessing import Queue
from threading import Thread
from typing import Optional, Callable, Iterable

import re

import datetime
import time
import pytz

import requests

from miner.execution.stop_initializer import StopInitializer
from miner.models import Stop, Departure, Line, TmpDeparture


def create_and_start_worker(worker_function: Callable, params: Iterable, worker_list: list):
    worker = Thread(target=worker_function, args=params)
    worker.setDaemon(True)
    worker.start()
    worker_list.append(worker)


class Conductor:
    # dict of stopIds with the time where it should next be fetched
    next_fetch_times = {}

    in_queue_marker = datetime.datetime(1970, 1, 1, 0, 0, 0, 0, pytz.utc)

    @staticmethod
    def prepare(with_coordinates=True):
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

        print('Finished preparation')

    def __init_fetch_times__(self):
        now = datetime.datetime.now().astimezone(pytz.utc)
        self.next_fetch_times = {stop.id: now for stop in Stop.objects.all()}

    def start(self):
        print('Starting workers')
        self.__init_fetch_times__()

        q = Queue()
        # init workers
        workers = []
        for _ in range(10):
            create_and_start_worker(self.__run_fetch_worker__, (q,), workers)

        # daemon to archive departures
        create_and_start_worker(self.__run_tmp_transfer_worker__, (), workers)

        # daemon to update lines every 6 hours
        create_and_start_worker(self.__run_update_lines_worker__, (), workers)

        print('Started {} workers, fetching starts now'.format(len(workers)))

        while True:
            now = datetime.datetime.now().astimezone(pytz.utc)

            # queue up needed stops
            for stop in self.next_fetch_times:
                fetch_time = self.next_fetch_times[stop]

                # only add the stop to work queue if we need to right now
                if now >= fetch_time > self.in_queue_marker:
                    self.next_fetch_times[stop] = self.in_queue_marker
                    q.put(stop)

            time.sleep(5)

    def __run_fetch_worker__(self, q: Queue):
        while True:
            try:
                self.__fetch_departure__(q)
            except:
                pass

    def __run_tmp_transfer_worker__(self):
        while True:
            tmpDeparturesLeft = 1
            try:
                tmpDeparturesLeft = self.__transfer_tmp_departures__()
            finally:
                if tmpDeparturesLeft < 1000:
                    time.sleep(60 * 10)

    def __run_update_lines_worker__(self):
        while True:
            time.sleep(60 * 60 * 6)
            try:
                self.prepare(with_coordinates=False)
            finally:
                pass

    @staticmethod
    def __transfer_tmp_departures__(enable_log=False):
        """
        after 30 minutes departures will never be touched again, so we transfer them to the archive
        :return: Number of elements left in the database
        """
        old_limit = datetime.datetime.now().astimezone(pytz.utc) - datetime.timedelta(minutes=30)
        tmp_departures = TmpDeparture.objects.filter(real_time__lte=old_limit)[:100]

        if enable_log:
            print("Going to transfer {} tmp departures".format(tmp_departures.count()))

        for tmp_departure in tmp_departures:
            # print("Transferring {}".format(tmp_departure.internal_id))

            Departure.objects.create(internal_id=tmp_departure.internal_id, stop=tmp_departure.stop,
                                     line=tmp_departure.line, scheduled_time=tmp_departure.scheduled_time,
                                     real_time=tmp_departure.real_time)
            tmp_departure.delete()

        return TmpDeparture.objects.count()

    def __fetch_departure__(self, q: Queue):
        # this line blocks until something is added to the queue
        stop_id = q.get()

        response = requests.get('https://webapi.vvo-online.de/dm',
                                {'limit': 10, 'mot': '[Tram, CityBus]', 'stopid': stop_id})

        # when fetching fails we wait 5 minute and try it again
        one_minute_wait_time = datetime.datetime.now().astimezone(pytz.utc) + datetime.timedelta(minutes=5)
        if response.status_code >= 400 or 'Departures' not in response.json():
            self.next_fetch_times[stop_id] = one_minute_wait_time
            return

        # longest wait time is 3 hours
        time_to_wait = datetime.datetime.now().astimezone(pytz.utc) + datetime.timedelta(hours=3)
        stop = Stop.objects.get(id=stop_id)

        for departure_json in response.json()['Departures']:
            departure = self.create_departure_from_json(departure_json, stop)

            if not departure:
                continue

            if departure.real_time < time_to_wait:
                time_to_wait = departure.real_time

        # always wait at least 60 seconds
        now = datetime.datetime.now(pytz.utc)
        if (time_to_wait - now) < datetime.timedelta(minutes=1):
            time_to_wait = now + datetime.timedelta(minutes=1)

        self.next_fetch_times[stop_id] = time_to_wait

    @staticmethod
    def create_departure_from_json(departure_json: dict, stop: Stop) -> Optional[TmpDeparture]:
        try:
            line = Line.objects.get_or_create(name=departure_json['LineName'], direction=departure_json['Direction'])[0]
            departure = TmpDeparture.objects.get_or_create(stop=stop, internal_id=departure_json['Id'], line=line)[0]
        except Exception:
            return None

        departure.scheduled_time = Conductor.parse_date_string_to_datetime(departure_json['ScheduledTime'])
        departure.real_time = Conductor.parse_date_string_to_datetime(
            departure_json['RealTime' if 'RealTime' in departure_json.keys() else 'ScheduledTime'])

        departure.save()
        return departure

    @staticmethod
    def parse_date_string_to_datetime(date: str) -> datetime:
        # TODO: extract this!
        p = re.match(r"/Date\((\d{13})([-|+]0\d)00\)/", date)

        if p:
            timestamp = int(p.group(1))
            timedelta = datetime.timedelta(hours=int(p.group(2)))
            return datetime.datetime.fromtimestamp(timestamp / 1000, datetime.timezone(timedelta))

        else:
            # TODO: why add a 2 hours time delta?
            return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').astimezone(
                datetime.timezone(datetime.timedelta(hours=2)))
