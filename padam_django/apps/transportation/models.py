from django.db import models
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError

class BusStop(models.Model):
    place = models.ForeignKey('geography.Place', on_delete=models.CASCADE)
    arrival_time = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self) -> str:
        arrival_time_str = self.arrival_time.strftime('%Y-%m-%d %H:%M')
        return f"BusStop: {self.place.name} arrive at: {arrival_time_str} (ID: {self.id})"

class BusShift(models.Model):
    bus = models.ForeignKey('fleet.Bus', on_delete=models.CASCADE)
    driver = models.ForeignKey('fleet.Driver', on_delete=models.CASCADE)
    stops = models.ManyToManyField(BusStop)

    def __str__(self) -> str:
        return f'Bus Shift: {self.bus.licence_plate} driven by {self.driver.user.username} (ID: {self.id})'

    @property
    def departure_time(self):
        """Returns the departure time of the bus shift, based on the earliest stop time."""
        if self.stops.exists():
            return self.stops.all().order_by('arrival_time').first().arrival_time
        return None

    @property
    def arrival_time(self):
        """Returns the arrival time of the bus shift, based on the latest stop time."""
        if self.stops.exists():
            return self.stops.all().order_by('arrival_time').last().arrival_time
        return None

    @property
    def shift_duration(self):
        """Calculates the total duration of the bus shift."""
        if self.departure_time and self.arrival_time:
            return self.arrival_time - self.departure_time
        return timedelta(0)