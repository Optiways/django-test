from django.db import models
from django.utils.datetime_safe import datetime
from django.utils.functional import cached_property

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

    @cached_property
    def departure(self) -> BusStop:
        return self.stops.order_by('time')[0]

    @cached_property
    def get_arrival(self) -> BusStop:
        return self.stops.order_by('-time')[0]

    @property
    def start_time(self) -> datetime:
        return self.departure.time

    @property
    def end_time(self) -> datetime:
        return self.get_arrival.time

    @property
    def duration(self):
        return self.end_time - self.start_time

    def __str__(self):
        return f"{self.driver} drive bus [{self.bus}] for {self.duration}, " \
               f"from {self.departure.place} to {self.get_arrival.place}"
