from django.db import models
from .validators import *


class BusShift(models.Model):
    bus = models.ForeignKey('fleet.Bus', on_delete=models.CASCADE, related_name='shift', blank=False)
    driver = models.ForeignKey('fleet.Driver', on_delete=models.CASCADE, related_name='shift', blank=False)
    stop = models.ManyToManyField('shift.BusStop', blank=False)

    def __str__(self):
        return f"Shift (id: {self.pk}) {self.bus} drive by {self.driver} - journey_duration: {self.journey_duration}"

    @property
    def departure(self):
        if len(self.stop.all()) > 0:
            first_stop = self.stop.all().order_by('stop_datetime').first()
            return first_stop.stop_datetime
        else:
            return None

    @property
    def arrival(self):
        if len(self.stop.all()) > 1:
            last_stop = self.stop.all().order_by('-stop_datetime').first()
            return last_stop.stop_datetime
        else:
            return None

    @property
    def journey_duration(self):
        if not any(prop is None for prop in (self.departure, self.arrival)):
            duration = (self.arrival - self.departure)
            return str(duration)
        else:
            return "not available"

class BusStop(models.Model):
    place = models.OneToOneField('geography.Place', on_delete=models.CASCADE)
    stop_datetime = models.DateTimeField("Stop time", validators=[validate_stop_datetime])

    def __str__(self):
        return f'Bus stop at {self.place.name} ({self.place.latitude}-{self.place.longitude}) at {self.stop_datetime}'
