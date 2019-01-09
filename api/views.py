import json

from django.core import serializers
from django.http import HttpResponse

from miner.models import Departure, Stop


def index(request):
    data = {
        'stop_count': Stop.objects.count(),
        'departure_count': Departure.objects.count(),
    }

    return HttpResponse(json.dumps(data), content_type='application/json')


def stops(request):
    return HttpResponse(serializers.serialize('json', Stop.objects.all()), content_type='application/json')
