from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='Status'),
    path('stops', views.stops, name='Stops')
]
