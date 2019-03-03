from django.test import TestCase
from unittest.mock import patch

from miner.execution.stop_initializer import StopInitializer
from miner.models import Stop, Line
from miner.tests.MockFunctions import LinesFromStopRequestMock, StopsFromLineRequestMock, StopsCoordinatesRequestMock


class StopInitializerTests(TestCase):
    def setUp(self):
        self.initializer = StopInitializer()
        self.initializer.initial_known_stops = [8080, 420]

    @patch('miner.execution.stop_initializer.requests', LinesFromStopRequestMock())
    def test_creating_lines_from_initial_stop(self):
        self.initializer.fetch_lines_from_initial_stops()

        self.assertEqual(Line.objects.filter(name='Line8080').count(), 1)
        self.assertEqual(Line.objects.filter(name='Line420').count(), 1)

    @patch('miner.execution.stop_initializer.requests', StopsFromLineRequestMock())
    def test_fetching_stops_from_found_lines(self):
        Line.objects.create(name='TestLine', direction='TestDirection', trip=5)

        self.initializer.fetch_stops_from_lines()
        self.assertEqual(Stop.objects.count(), 3)

    @patch('miner.execution.stop_initializer.requests', StopsFromLineRequestMock())
    def test_fetching_stops_from_found_lines_with_invalid_trip_id(self):
        line = Line.objects.create(name='TestLine', direction='TestDirection', trip=7)

        self.initializer.fetch_stops_from_lines()
        self.assertEqual(Stop.objects.count(), 0)

        line.refresh_from_db()
        self.assertEqual(line.trip, 0)

    @patch('miner.execution.stop_initializer.requests', StopsCoordinatesRequestMock())
    def test_fetch_coordinates_of_stop(self):
        stop501 = Stop.objects.create(id=501, name='TestStop1')
        stop502 = Stop.objects.create(id=502, name='TestStop2')

        init_x_coordinate = 5891
        init_y_coordinate = 9401
        stop503 = Stop.objects.create(id=503, name='TestStop2', x_coordinate=init_x_coordinate,
                                      y_coordinate=init_y_coordinate)

        self.initializer.fetch_stop_coordinates()

        stop501.refresh_from_db()
        stop502.refresh_from_db()
        stop503.refresh_from_db()

        # coordinates should update
        self.assertEqual(stop501.x_coordinate, 4595301)
        self.assertEqual(stop501.y_coordinate, 5687866)

        # coordinates should stay empty because server throws an error
        self.assertEqual(stop502.x_coordinate, 0)
        self.assertEqual(stop502.y_coordinate, 0)

        # coordinates should stay empty because they are already set
        self.assertEqual(stop503.x_coordinate, init_x_coordinate)
        self.assertEqual(stop503.y_coordinate, init_y_coordinate)
