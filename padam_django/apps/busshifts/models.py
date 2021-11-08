from django.db import models
from django.utils.datetime_safe import datetime

from padam_django.apps.fleet.models import Bus, Driver
from padam_django.apps.geography.models import Place


class BusStop(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    time = models.DateTimeField()

    def __str__(self):
        return f"Stop at {self.place}, {self.time}"


class BusShift(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    stops = models.ManyToManyField(BusStop)

    def get_departure(self) -> BusStop:
        return self.stops.order_by('time')[0]

    def get_arrival(self) -> BusStop:
        return self.stops.order_by('-time')[0]

    def get_start_time(self) -> datetime:
        return self.get_departure().time

    def get_end_time(self) -> datetime:
        return self.get_arrival().time

    def get_duration(self):
        return self.get_end_time() - self.get_start_time()

    def __str__(self):
        return f"{self.driver} drive bus [{self.bus}] for {self.get_duration()}, " \
               f"from {self.get_departure().place} to {self.get_arrival().place}"
