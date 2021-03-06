from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='Status'),
    path('stops', views.stops, name='Stops'),
    path('stops-of-lines', views.lines_with_stops),
    path('departure', views.departure)
]
