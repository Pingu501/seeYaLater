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
