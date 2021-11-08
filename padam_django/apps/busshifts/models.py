from django.db import models

from padam_django.apps.fleet.models import Bus, Driver
from padam_django.apps.geography.models import Place


class BusShift(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    stops = models.ManyToManyField("BusStop")

    def get_start_time(self):
        return self.stops.order_by('time')[0].time

    def get_end_time(self):
        return self.stops.order_by('-time')[0].time

    def get_duration(self):
        return self.get_end_time() - self.get_start_time()

    def __str__(self):
        return f"{self.get_duration()}"


class BusStop(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    time = models.DateTimeField()

    def __str__(self):
        return f"Stop at {self.place}, {self.time}"
