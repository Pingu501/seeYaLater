import datetime
from queue import Queue

import pytz
from django.test import TestCase
from unittest.mock import patch

from miner.execution.conductor import Conductor
from miner.models import Departure, Line, Stop, TmpDeparture
from miner.tests.MockFunctions import FetchDeparturesRequestMock


class ConductorTests(TestCase):

    def setUp(self):
        self.conductor = Conductor()

        self.q = Queue()

        # create dummy stops
        [Stop.objects.create(name='Test' + str(i), id=i) for i in range(110, 120)]

    @patch('miner.execution.conductor.requests', FetchDeparturesRequestMock)
    def test_fetch_departure_success(self):
        self.q.put(110)

        self.conductor.__fetch_departure__(self.q)

        self.assertTrue(self.q.empty())
        self.assertEqual(len(self.conductor.next_fetch_times), 1)
        self.assertTrue(110 in self.conductor.next_fetch_times)
        self.assertEqual(TmpDeparture.objects.count(), 2)

    @patch('miner.execution.conductor.requests', FetchDeparturesRequestMock)
    def test_fetch_departure_too_short_wait_times(self):
        self.q.put(111)

        self.conductor.__fetch_departure__(self.q)

        next_fetch_time = self.conductor.next_fetch_times.get(111)
        self.assertIsNotNone(next_fetch_time)

        calc_next_fetch = datetime.datetime.now().astimezone(pytz.utc) + datetime.timedelta(seconds=50)
        self.assertTrue((next_fetch_time - calc_next_fetch).seconds <= 10)
        self.assertEqual(TmpDeparture.objects.count(), 1)

    @patch('miner.execution.conductor.requests', FetchDeparturesRequestMock)
    def test_fetch_departure_with_empty_response(self):
        self.q.put(112)

        self.conductor.__fetch_departure__(self.q)
        self.assertEqual(Departure.objects.count(), 0)
        self.assertEqual(TmpDeparture.objects.count(), 0)

    @patch('miner.execution.conductor.requests', FetchDeparturesRequestMock)
    def test_fetch_departure_with_missing_departures(self):
        self.q.put(113)

        self.conductor.__fetch_departure__(self.q)
        self.assertEqual(Departure.objects.count(), 0)
        self.assertEqual(TmpDeparture.objects.count(), 0)

    @patch('miner.execution.conductor.requests', FetchDeparturesRequestMock)
    def test_fetch_departure_with_server_error(self):
        self.q.put(114)

        self.conductor.__fetch_departure__(self.q)
        self.assertEqual(Departure.objects.count(), 0)
        self.assertEqual(TmpDeparture.objects.count(), 0)

    def test_create_departure_from_valid_json(self):
        time = datetime.datetime.now().astimezone(datetime.timezone(datetime.timedelta(hours=2)))
        time_as_string = time.strftime('%Y-%m-%d %H:%M:%S')

        stop = Stop.objects.get(id=110)

        departure = self.conductor.create_departure_from_json({
            'LineName': 'newTestLine',
            'Direction': 'newTestDirection',
            'Id': 501,
            'ScheduledTime': time_as_string,
            'RealTime': time_as_string
        }, stop)

        self.assertEqual(Line.objects.count(), 1, 'There should be exactly one line created!')
        line = Line.objects.first()
        self.assertEqual(line.name, 'newTestLine', 'Wrong line in database!')
        self.assertEqual(departure.line, line)

        self.assertEqual(departure.stop, stop)

    def test_create_departure_from_invalid_json(self):
        self.assertIsNone(self.conductor.create_departure_from_json({
            'Feaf': 'newTestLine',
            'faw': 'newTestDirection',
        }, Stop.objects.get(id=110)))

    def test_tmp_departure_transfer_for_past_departures(self):
        stop = Stop.objects.create(id=3000, name='Test Stop')
        line = Line.objects.create(name='TestLine', direction='Test')

        time = datetime.datetime.now().astimezone(pytz.utc) - datetime.timedelta(minutes=70)

        TmpDeparture.objects.create(internal_id=500, stop=stop, line=line, scheduled_time=time, real_time=time)
        self.assertEqual(TmpDeparture.objects.count(), 1)

        self.conductor.__transfer_tmp_departures__(run_endless=False)

        self.assertEqual(TmpDeparture.objects.count(), 0)
        self.assertEqual(Departure.objects.count(), 1)

    def test_tmp_departure_transfer_for_future_departures(self):
        stop = Stop.objects.create(id=3001, name='Test Stop')
        line = Line.objects.create(name='TestLine', direction='Test')

        time = datetime.datetime.now().astimezone(pytz.utc) + datetime.timedelta(minutes=70)

        TmpDeparture.objects.create(internal_id=501, stop=stop, line=line, scheduled_time=time, real_time=time)
        self.assertEqual(TmpDeparture.objects.count(), 1)

        self.conductor.__transfer_tmp_departures__(run_endless=False)

        self.assertEqual(TmpDeparture.objects.count(), 1)
        self.assertEqual(Departure.objects.count(), 0)
