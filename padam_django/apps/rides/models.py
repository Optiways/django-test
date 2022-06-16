from django.db import models
import datetime


class BusShift(models.Model):
    bus = models.ForeignKey('fleet.Bus', null=True, on_delete=models.CASCADE)
    driver = models.ForeignKey('fleet.Driver', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Shift: {self.bus.licence_plate} - {self.driver.user.username} (id: {self.pk})"

class BusStop(models.Model):
    place = models.ForeignKey('geography.Place', null=True, on_delete=models.CASCADE)
    time = models.DateTimeField('arrival time', null=True)
    stop = models.PositiveIntegerField()
    busshift = models.ForeignKey(BusShift, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Stop: {self.stop} - {self.place.name} (id: {self.pk})"