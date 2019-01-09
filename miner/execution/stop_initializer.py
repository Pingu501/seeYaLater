from datetime import datetime, timezone

import re
import requests

from miner.models import Line, Stop, StopsOfLine


class StopInitializer:
    initial_known_stops = [33000005, 33000007, 33000028, 33000115, 33000727, 33000052, 33000111, 33000742, 33000037,
                           33000144]

    def fetch_lines_from_initial_stops(self):
        """
        This will look for the next 30 lines driving threw each of the initial known stops
        """

        for stop_id in self.initial_known_stops:
            response = requests.post('https://webapi.vvo-online.de/dm',
                                     {'stopid': stop_id, 'mot': '[Tram, CityBus]', 'limit': 30})
            json = response.json()

            for departure in json['Departures']:
                line = Line.objects.get_or_create(name=departure['LineName'], direction=departure['Direction'])[0]
                line.trip = departure['Id']
                line.save()

    def fetch_stops_from_lines(self):
        """
        In fetch_lines_from_initial_stops the route of each line is sent which we use to find all
        stops for the line. Combined with all lines we should be able to get all stops

        :return: void
        """
        now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

        for line in Line.objects.all():
            if line.trip == 0:
                continue

            # the stop id is required and tells whether the delivered stops are before or after this one
            # not used by us at the moment
            post_fields = {'tripId': line.trip, 'time': now, 'stopId': self.initial_known_stops[0]}

            response = requests.post('https://webapi.vvo-online.de/dm/trip', post_fields)

            if response.status_code >= 400:
                print('Error fetching line {} got {}'.format(line.name, response.json()))
                continue

            stop_number = 0
            for stop_raw in response.json()['Stops']:
                stop = Stop.objects.get_or_create(id=stop_raw['Id'])[0]
                stop.name = stop_raw['Name']
                stop.save()

                StopsOfLine.objects.get_or_create(stop=stop, line=line, position=stop_number)

                stop_number += 1

    @staticmethod
    def fetch_stop_coordinates():
        for stop in Stop.objects.all():
            if stop.x_coordinate != 0 and stop.y_coordinate != 0:
                continue

            response = requests.post('https://webapi.vvo-online.de/tr/pointfinder', {'query': stop.id})

            # first hit should always be the right stop
            result = response.json()['Points'][0]
            p = re.match(r"\d{8}\|\|\|?.*\|(\d*)\|(\d*)\|\d*\|\|", result)

            try:
                stop.x_coordinate = p.group(1)
                stop.y_coordinate = p.group(2)
                stop.save()
            except:
                print('Error while parsing: ', result)
