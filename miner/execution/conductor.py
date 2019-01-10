from multiprocessing import Queue
from threading import Thread

from typing import Optional

import re

import datetime
import time
import pytz

import requests

from miner.execution.stop_initializer import StopInitializer
from miner.models import Stop, Departure, Line


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
        for _ in range(20):
            worker = Thread(target=self.__fetch_departure__, args=(q,))
            worker.setDaemon(True)
            worker.start()
            workers.append(worker)

        while True:
            now = datetime.datetime.now().astimezone(pytz.utc)

            # queue up needed stops
            for stop in self.next_fetch_times:
                fetch_time = self.next_fetch_times[stop]

                # only add the stop to work queue if we need to right now
                if now >= fetch_time > self.in_queue_marker:
                    self.next_fetch_times[stop] = self.in_queue_marker
                    q.put(stop)

            # restart all failed workers
            for worker in workers:
                if not worker.is_alive():
                    worker.start()

            time.sleep(5)

    def __fetch_departure__(self, q: Queue):
        while True:
            # this line blocks until something is added to the queue
            stop_id = q.get()

            response = requests.get('https://webapi.vvo-online.de/dm',
                                    {'limit': 10, 'mot': '[Tram, CityBus]', 'stopid': stop_id})

            # TODO: fail strategy!
            if response.status_code >= 400:
                if 'Status' in response.json() and 'Message' in response.json()['Status']:
                    if 'service not available' in response.json()['Status']['Message']:
                        print('Service is down')
                        time.sleep(20)

                        # add stop again to queue and try again
                        q.put(stop_id)
                        continue

                    print(response.json()['Status']['Message'])
                else:
                    print('Some undefined error occurred: ', response.json())

                continue

            if 'Departures' not in response.json():
                continue

            time_to_wait = datetime.datetime.now().astimezone(pytz.utc) + datetime.timedelta(1)
            stop = Stop.objects.get(id=stop_id)

            for departure_json in response.json()['Departures']:
                departure = self.create_departure_from_json(departure_json, stop)

                if not departure:
                    continue

                if departure.real_time < time_to_wait:
                    time_to_wait = departure.real_time

            # always wait at least 60 seconds
            now = datetime.datetime.now(pytz.utc)
            if time_to_wait - now < datetime.timedelta(0, 60):
                time_to_wait = now + datetime.timedelta(0, 60)

            self.next_fetch_times[stop_id] = time_to_wait

    @staticmethod
    def create_departure_from_json(departure_json: dict, stop: Stop) -> Optional[Departure]:
        try:
            line = Line.objects.get_or_create(name=departure_json['LineName'], direction=departure_json['Direction'])[0]
            departure = Departure.objects.get_or_create(stop=stop, internal_id=departure_json['Id'], line=line)[0]
        except Exception:
            return None

        departure.scheduled_time = Conductor.parse_date_string_to_datetime(departure_json['ScheduledTime'])
        departure.real_time = Conductor.parse_date_string_to_datetime(
            departure_json['RealTime' if 'RealTime' in departure_json.keys() else 'ScheduledTime'])

        departure.save()
        return departure

    @staticmethod
    def parse_date_string_to_datetime(date: str) -> datetime:
        p = re.match(r"/Date\((\d{13})([-|+]0\d)00\)/", date)

        if p:
            timestamp = int(p.group(1))
            timedelta = datetime.timedelta(hours=int(p.group(2)))
            return datetime.datetime.fromtimestamp(timestamp / 1000, datetime.timezone(timedelta))

        else:
            return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').astimezone(
                datetime.timezone(datetime.timedelta(hours=2)))
