import json

from django.core.cache import cache
from django.http import HttpResponse

from miner.models import Departure, Stop, Line, StopsOfLine, TmpDeparture


def index(request):
    data = {
        'stop_count': Stop.objects.count(),
        'departure_count': Departure.objects.count(),
        'tmp_departure_count': TmpDeparture.objects.count()
    }

    return HttpResponse(json.dumps(data), content_type='application/json')


def stops(request):
    found_stops = cache.get('view_get_stops')

    if not found_stops:
        found_stops = [{
            'id': stop.id,
            'name': stop.name,
            'x': stop.x_coordinate,
            'y': stop.y_coordinate
        } for stop in Stop.objects.all()]

        cache.set('view_get_stops', found_stops)

    return HttpResponse(json.dumps(found_stops), content_type='application/json')


def lines_with_stops(request):
    """
    :param request:
    :return:
    """
    all_lines_with_stops = cache.get('view_lines_with_stops')

    if not all_lines_with_stops:
        print('cache not set')
        all_lines_with_stops = []
        lines = Line.objects.all().order_by('name')

        for line in lines:
            stops_of_line = [stopOfLine.stop.id for stopOfLine in
                             StopsOfLine.objects.filter(line=line).order_by('position')]
            if len(stops_of_line) == 0:
                continue

            all_lines_with_stops.append({
                'line': line.name,
                'direction': line.direction,
                'stops': stops_of_line
            })

        cache.set('view_lines_with_stops', all_lines_with_stops)

    return HttpResponse(json.dumps(all_lines_with_stops), content_type='application/json')


def departure(request):
    """
    Get all departures for the request
    :param request: needs stopId, time and limit
    :return:
    """
    stop_id = request.GET['stop_id']
    # departure_time = request.GET['time'] if request.GET['time'] else None
    # limit = request.GET['limit'] if request.GET['limit'] else 10

    if not stop_id:
        return __bad_request_response('Parameter stop_id is required')

    departures = TmpDeparture.objects.filter(stop=stop_id).order_by('-real_time')[:20]

    return HttpResponse(json.dumps([{
        'id': e.id,
        'scheduled': e.scheduled_time.timestamp(),
        'real': e.real_time.timestamp(),
        'line': e.line.name,
        'direction': e.line.direction
    } for e in departures]), content_type='application/json')


def __bad_request_response(text):
    return HttpResponse(text, status=400)
