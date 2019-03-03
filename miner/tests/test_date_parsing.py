import datetime

# use TestCase from unittest to remove database overhead
from unittest import TestCase

from miner.execution.conductor import Conductor


class DateParsingTest(TestCase):

    def setUp(self):
        self.conductor = Conductor()

    def test_date_parsing_dvb_departure_offset_2(self):
        parsed_date_time = self.conductor.parse_date_string_to_datetime('/Date(1551618211875+0000)/')

        self.assertEqual(parsed_date_time.year, 2019)
        self.assertEqual(parsed_date_time.month, 3)
        self.assertEqual(parsed_date_time.day, 3)
        self.assertEqual(parsed_date_time.hour, 13)
        self.assertEqual(parsed_date_time.minute, 3)
        self.assertEqual(parsed_date_time.second, 31)
        self.assertEqual(parsed_date_time.microsecond, 875000)

        self.assertEqual(parsed_date_time.tzinfo.utcoffset(None), datetime.timedelta(seconds=60 * 60 * 0))

    def test_date_parsing_dvb_departure_offset_1(self):
        parsed_date_time = self.conductor.parse_date_string_to_datetime('/Date(1551618211875+0100)/')

        self.assertEqual(parsed_date_time.year, 2019)
        self.assertEqual(parsed_date_time.month, 3)
        self.assertEqual(parsed_date_time.day, 3)
        self.assertEqual(parsed_date_time.hour, 14)
        self.assertEqual(parsed_date_time.minute, 3)
        self.assertEqual(parsed_date_time.second, 31)
        self.assertEqual(parsed_date_time.microsecond, 875000)

        # 1 hour shift from the timezone
        self.assertEqual(parsed_date_time.tzinfo.utcoffset(None), datetime.timedelta(seconds=60 * 60 * 1))

    def test_date_parsing_dvb_departure_offset_2(self):
        parsed_date_time = self.conductor.parse_date_string_to_datetime('/Date(1551618211875+0200)/')

        self.assertEqual(parsed_date_time.year, 2019)
        self.assertEqual(parsed_date_time.month, 3)
        self.assertEqual(parsed_date_time.day, 3)
        self.assertEqual(parsed_date_time.hour, 15)
        self.assertEqual(parsed_date_time.minute, 3)
        self.assertEqual(parsed_date_time.second, 31)
        self.assertEqual(parsed_date_time.microsecond, 875000)

        # 2 hour shift from the timezone
        self.assertEqual(parsed_date_time.tzinfo.utcoffset(None), datetime.timedelta(seconds=60 * 60 * 2))
