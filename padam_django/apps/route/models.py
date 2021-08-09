from datetime import datetime

from django.db import models


class BusStop(models.Model):
    name = models.CharField(max_length=50)
    place = models.OneToOneField('geography.Place', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Stop: {self.name} located at {self.place} ({self.place.latitude}, {self.place.longitude})"


class BusShift(models.Model):
    bus = models.ForeignKey('fleet.Bus', on_delete=models.CASCADE, related_name='shifts')
    driver = models.ForeignKey('fleet.Driver', on_delete=models.CASCADE, null=True, related_name='shifts')
    stops = models.ManyToManyField('route.BusStopDate')

    def __str__(self) -> str:
        return f"Shift #{self.pk} {self.bus} drived by {self.driver}"

    @property
    def departure(self) -> datetime:
        first_stop = self.stops.first()

        return first_stop.date if first_stop else None

    @property
    def arrival(self) -> datetime:
        last_stop = self.stops.last()

        return last_stop.date if last_stop else None

    @property
    def duration(self) -> datetime:
        total_duration = abs(self.arrival - self.departure)
        hours = total_duration.seconds // 3600
        minutes = (total_duration.seconds // 60) % 60

        return f"{hours} hours, {minutes} minutes"


class BusStopDate(models.Model):
    stop = models.ForeignKey('route.BusStop', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField()

    class Meta:
        ordering = ['date']

    def __str__(self) -> str:
        return f"{self.stop} at {self.date}"