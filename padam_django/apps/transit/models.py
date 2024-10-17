from datetime import datetime, timedelta

from django.db import models
from django.utils import timezone

from padam_django.apps.geography.models import Place


class BusShift(models.Model):
    """
        Model representing a bus shift
    """
    bus = models.ForeignKey('fleet.Bus', null=False, blank=False, on_delete=models.CASCADE)
    driver = models.ForeignKey("fleet.Driver", null=False, blank=False, on_delete=models.CASCADE)

    @property
    def departure_stop(self) -> str:
        """ Retrieve the departure stop name"""
        return self.stops.all().order_by("transit_time").first().place.name

    @property
    def arrival_stop(self) -> str:
        """ Retrieve the departure arrival name"""
        return self.stops.all().order_by("transit_time").first().place.name

    @property
    def departure_time(self) -> datetime:
        """ Retrieve the departure time of the bus shift"""
        return self.stops.all().order_by("transit_time").first().transit_time

    @property
    def arrival_time(self) -> datetime:
        """ Retrieve the arrival time of the bus shift"""
        return self.stops.all().order_by("transit_time").last().transit_time

    @property
    def shift_duration(self) -> timedelta:
        """ Retrieve the transit duration of the bus shift"""
        if self.arrival_time and self.departure_time:
            return self.arrival_time - self.departure_time

    @property
    def is_in_transit(self) -> bool:
        """ Check if the bus shift is currently in a transit """
        return self.departure_time < timezone.now() < self.arrival_time

    @property
    def has_transit_not_started(self) -> bool:
        """ Check if the bus shift has started """
        return timezone.now() < self.departure_time

    def can_add_stop(self, time: datetime) -> bool:
        """ Check if it's possible to add a stop """
        return (self.is_in_transit or self.has_transit_not_started) and time > timezone.now()

    def __str__(self):
        return f"{self.bus} - {self.departure_stop} - {self.arrival_stop}"


class BusStop(models.Model):
    """ 
    	Model representing a bus stop 
		Each bus stop is a child of a specific bus shift
    """
    place = models.ForeignKey(Place, null=False, blank=False, on_delete=models.CASCADE)
    transit_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    bus_shift = models.ForeignKey(BusShift, related_name="stops", null=False, blank=False, on_delete=models.CASCADE)

    def can_modify_stop(self, time: datetime) -> bool:
        """ Check if it's possible to modify a stop '"""
        return self.transit_time > timezone.now() < time

    def __str__(self):
        return f"{self.place.name} {self.transit_time}"
