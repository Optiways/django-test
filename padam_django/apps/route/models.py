from datetime import datetime
from typing import Optional

from django.db import models


class BusStop(models.Model):
    """A model representing a bus stop."""
    place = models.ForeignKey('geography.Place', on_delete=models.CASCADE)
    transit_time = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self) -> str:
        """Returns a string representation of a BusStop instance."""
        transit_time_str = self.transit_time.strftime('%m/%d/%Y %H:%M')
        return f"Bus Stop: {self.place.name} - {transit_time_str} (id: {self.pk})"


class BusShift(models.Model):
    """A model representing a bus shift."""
    bus = models.ForeignKey('fleet.Bus', on_delete=models.CASCADE, null=False, blank=False)
    driver = models.ForeignKey('fleet.Driver', on_delete=models.CASCADE, null=False, blank=False,)
    stops = models.ManyToManyField('BusStop', related_name='bus_shifts', blank=True)

    @property
    def departure_time(self) -> Optional[datetime]:
        """Returns the departure time of the bus shift."""
        if self.stops.exists():
            return self.stops.all().order_by('transit_time').first().transit_time
        else:
            return None

    @property
    def arrival_time(self) -> Optional[datetime]:
        """Returns the arrival time of the bus shift."""
        if self.stops.exists():
            return self.stops.all().order_by('transit_time').last().transit_time
        else:
            return None

    @property
    def shift_duration(self) -> Optional[datetime]:
        """Returns the duration of the bus shift."""
        if self.stops.exists():
            return self.arrival_time - self.departure_time
        else:
            return None

    def __str__(self) -> str:
        """Returns a string representation of a BusShift instance."""
        return f'Bus Shift: Bus:{self.bus.licence_plate}, Driver: {self.driver.user.username} (id: {self.pk})'
