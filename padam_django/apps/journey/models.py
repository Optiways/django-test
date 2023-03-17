from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q


class BusShift(models.Model):
    bus = models.ForeignKey(
        'buses.bus', on_delete=models.CASCADE, related_name='shift')
    driver = models.ForeignKey(
        'drivers.driver', on_delete=models.CASCADE, related_name='shift')
    bus_stops = models.ManyToManyField('BusStop', related_name='bus_shifts')

    def save(self, *args, **kwargs):
        # Check if the bus shift has at least two bus stops
        if self.bus_stops.count() < 2:
            raise ValueError("A bus shift must have at least two bus stops.")
        # Set the start time to the passing time of the first bus stop
        first_bus_stop = self.bus_stops.order_by('passing_time').first()
        self.start_time = first_bus_stop.passing_time

        # Set the end time to the passing time of the last bus stop
        last_bus_stop = self.bus_stops.order_by('-passing_time').first()
        self.end_time = last_bus_stop.passing_time
        self.shift_duration = self.end_time - self.start_time

        # Check if the same bus is already assigned to another shift at the
        # same time
        # this here is to find the busshift that has the same bus fixed
        # with time overlapping
        if BusShift.objects.filter(
            Q(bus=self.bus) | Q(driver=self.driver)).filter(
                start_time__lte=self.end_time, end_time__gte=self.start_time).exclude(
                pk=self.pk).exists():
            raise ValidationError(
                'This bus is already assigned to another shift at this time.')

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Driver: {self.user.username} (id: {self.pk})"


class BusStop(models.Model):
    place = models.OneToOneField(
        'places.Place', on_delete=models.CASCADE, related_name='driver')
    passing_time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"Place: {self.place.name} (id: {self.pk})"
