from datetime import datetime
from django.db import models


class BusShift(models.Model):
    bus = models.ForeignKey('fleet.Bus', on_delete=models.CASCADE, related_name='shifts')
    driver = models.ForeignKey('fleet.Driver', on_delete=models.CASCADE, related_name='shifts')
    stop = models.ManyToManyField('shifts.BusTravelTime')

    def __str__(self):
        return f"Shift {self.bus} drive by {self.driver}"

    @property
    def departure(self):
        first_stop = self.stop.first()
        if first_stop:
            return first_stop.date
        else:
            return None

    @property
    def arrival(self):
        last_stop = self.stop.last()
        if last_stop:
            return last_stop.date
        else:
            return None

    @property
    def travel_time(self):
        time = abs(self.arrival - self.departure)
        hours = time.seconds // 3600
        minutes = (time.seconds // 60) % 60

        return f"{hours} hours, {minutes} minutes"


class BusStop(models.Model):
    name = models.CharField('Bus stop name', max_length=100)
    place = models.OneToOneField('geography.Place', on_delete=models.CASCADE)

    def __str__(self):
        return f'Bus stop {self.name} at {self.place.name} {self.place.latitude} {self.place.longitude}'


class BusTravelTime(models.Model):
    stop = models.ForeignKey('shifts.BusStop', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField()

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f'{self.stop} at {self.date}'
