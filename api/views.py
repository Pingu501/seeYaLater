import json

from django.http import HttpResponse

from miner.models import Departure, Stop, Line, StopsOfLine


def index(request):
    data = {
        'stop_count': Stop.objects.count(),
        'departure_count': Departure.objects.count(),
    }

    return HttpResponse(json.dumps(data), content_type='application/json')


def stops(request):
    list_of_stops = {}

    for stop in Stop.objects.all():
        list_of_stops[stop.id] = {
            'id': stop.id,
            'name': stop.name,
            'x': stop.x_coordinate,
            'y': stop.y_coordinate,
            'connections': [{
                'stop_id': connection.stop.id,
                'line': connection.line.name,
                'direction': connection.line.direction
            } for connection in StopsOfLine.objects.filter(stop=stop)]
        }

    return HttpResponse(json.dumps(list_of_stops), content_type='application/json')


def lines_with_stops(request):
    """
    !!!unused!!!
    :param request:
    :return:
    """
    all_lines_with_stops = []
    lines = Line.objects.all().order_by('name')

    for line in lines:
        stops_of_line = [stopOfLine.stop.id for stopOfLine in StopsOfLine.objects.filter(line=line).order_by('position')]
        if len(stops_of_line) == 0:
            continue

        all_lines_with_stops.append({
            'line': line.name,
            'direction': line.direction,
            'stops': stops_of_line
        })

    return HttpResponse(json.dumps(all_lines_with_stops), content_type='application/json')
