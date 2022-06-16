from django.db import models
import datetime


class BusStop(models.Model):
    bus = models.ForeignKey('fleet.Bus', null=True, on_delete=models.CASCADE)
    place = models.ForeignKey('geography.Place', null=True, on_delete=models.CASCADE)
    time = models.DateTimeField('arrival time', null=True)
    stop = models.PositiveIntegerField()

    def __str__(self):
        return f"Stop: {self.stop}-{self.place.name} Bus: {self.bus.licence_plate} (id: {self.pk})"