from datetime import datetime, timezone

import requests

from miner.models import Line, Stop, StopsOfLine


class StopInitializer:
    initial_known_stops = [33000005, 33000007, 33000028, 33000115, 33000727, 33000052, 33000111, 33000742]

    def fetch_lines_from_initial_stops(self):
        """
        this will look for the next 30 lines driving threw each of the initial known stops

        :return: list of all found lines
        """

        for stop_id in self.initial_known_stops:
            response = requests.get('https://webapi.vvo-online.de/dm',
                                    {'stopid': stop_id, 'mot': '[Tram, CityBus]', 'limit': 30})
            json = response.json()

            for departure in json['Departures']:
                try:
                    Line.objects.get(name=departure['LineName'], direction=departure['Direction'])
                except Line.DoesNotExist:
                    Line.objects.create(name=departure['LineName'], direction=departure['Direction'],
                                        trip=departure['Id'])

    def fetch_stops_from_lines(self):
        now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

        for line in Line.objects.all():
            # no clue what stop id is for in this request, but is required
            post_fields = {'tripId': line.trip, 'time': now, 'stopId': self.initial_known_stops[0]}

            response = requests.get('https://webapi.vvo-online.de/dm/trip', post_fields)

            stop_number = 0
            for stop_raw in response.json()['Stops']:
                try:
                    stop = Stop.objects.get(id=stop_raw['Id'])
                except Stop.DoesNotExist:
                    stop = Stop.objects.create(id=stop_raw['Id'], name=stop_raw['Name'])

                StopsOfLine.objects.get_or_create(stop=stop, line=line, position=stop_number)
                stop_number += 1
