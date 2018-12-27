from django.db import models


class Stop(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)

    x_coordinate = models.IntegerField(default=0)
    y_coordinate = models.IntegerField(default=0)


class Line(models.Model):
    name = models.CharField(max_length=18)
    direction = models.CharField(max_length=200)

    # with the trip id we get a list of all stops this line serves
    trip = models.IntegerField(default=0)


class Departure(models.Model):
    internal_id = models.IntegerField()
    stop = models.ForeignKey(Stop, on_delete=models.DO_NOTHING)
    line = models.ForeignKey(Line, on_delete=models.DO_NOTHING)

    scheduled_time = models.DateTimeField('scheduled time', null=True)
    real_time = models.DateTimeField('real time', null=True)


class StopsOfLine(models.Model):
    line = models.ForeignKey(Line, on_delete=models.CASCADE)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    position = models.IntegerField()
