import datetime

import pytz


class Response:
    def __init__(self, response, status_code=200):
        self.response = response
        self.status_code = status_code

    def json(self):
        return self.response


class LinesFromStopRequestMock:
    @staticmethod
    def post(path, arguments):
        stopId = str(arguments['stopid'])
        return Response({
            'Departures': [
                {
                    'LineName': 'Line' + stopId,
                    'Direction': 'Direction' + stopId,
                    'Trip': 5
                }
            ]
        }, 200)


class StopsFromLineRequestMock:
    @staticmethod
    def post(path, arguments):
        if arguments['tripId'] == 5:
            return Response({
                'Stops': [
                    {
                        'Id': 501,
                        'Name': 'Test1'
                    },
                    {
                        'Id': 502,
                        'Name': 'Test2'
                    },
                    {
                        'Id': 503,
                        'Name': 'Test3'
                    }
                ]
            })
        else:
            return Response({}, status_code=500)


class StopsCoordinatesRequestMock:
    @staticmethod
    def post(path, arguments):
        if arguments['query'] == 501:
            return Response({
                'Points': [
                    '33005750||City|StationName|5687866|4595301|0||'
                ]
            })

        if arguments['query'] == 502:
            return Response({}, 400)


class FetchDeparturesRequestMock:
    @staticmethod
    def get(path, arguments):
        if arguments['stopid'] == 110:
            time = datetime.datetime.now().astimezone(datetime.timezone(datetime.timedelta(hours=2)))
            time_as_string = time.strftime('%Y-%m-%d %H:%M:%S')

            return Response({
                'Departures': [
                    {
                        'LineName': 'newTestLine',
                        'Direction': 'newTestDirection',
                        'Id': 1001,
                        'ScheduledTime': time_as_string,
                        'RealTime': time_as_string
                    },
                    {
                        'LineName': 'SecondTestLine',
                        'Direction': 'SecondTestDirection',
                        'Id': 1002,
                        'ScheduledTime': time_as_string,
                        'RealTime': time_as_string
                    }
                ]
            })

        if arguments['stopid'] == 111:
            scheduled_time = datetime.datetime.now().astimezone(pytz.utc)
            real_time = scheduled_time + datetime.timedelta(seconds=40)

            return Response({
                'Departures': [
                    {
                        'LineName': 'SecondTestLine',
                        'Direction': 'SecondTestDirection',
                        'Id': 1002,
                        'ScheduledTime': scheduled_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'RealTime': real_time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                ]
            })

        if arguments['stopid'] == 112:
            return Response({'Departures': []})

        if arguments['stopid'] == 113:
            return Response({})

        if arguments['stopid'] == 114:
            return Response({}, 500)
