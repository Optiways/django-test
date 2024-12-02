from django.db import models
from django.core.exceptions import ValidationError

from padam_django.apps.fleet.models import Bus, Driver
from padam_django.apps.geography.models import Place

from datetime import datetime, timedelta
from django.utils import timezone


class BusShift(models.Model):
    BusShiftname = models.CharField("Name of the Bus Shift",
                                    max_length=100, default="Shift")

    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

    shift_start = models.DateTimeField(default=timezone.now())
    shift_end = models.DateTimeField(
        default=timezone.now() + timedelta(hours=8))

    places = models.ManyToManyField(Place, related_name='bus_shifts')

    @property
    def duration(self):
        return self.shift_end - self.shift_start

    class Meta:
        verbose_name_plural = "Bus Shifts"

    def __str__(self):
        return f"Bus Shift: {self.BusShiftname}"

    def clean(self):
        # Validate that the bus is not already assigned to another shift during the same period
        overlapping_shifts = BusShift.objects.filter(
            bus=self.bus,
            shift_start__lt=self.shift_end,
            shift_end__gt=self.shift_start
        ).exclude(id=self.id)
        if overlapping_shifts.exists():
            raise ValidationError(
                'This bus is already assigned to another shift during the selected time period.')

        # Validate that the driver is not already assigned to another shift during the same period
        overlapping_shifts = BusShift.objects.filter(
            driver=self.driver,
            shift_start__lt=self.shift_end,
            shift_end__gt=self.shift_start
        ).exclude(id=self.id)
        if overlapping_shifts.exists():
            raise ValidationError(
                'This driver is already assigned to another shift during the selected time period.')

    def save(self, *args, **kwargs):
        self.clean()  # Ensure clean is called to validate before saving
        super().save(*args, **kwargs)


# class BusStops(models.Model):

#     bus_line = models.CharField(max_length=100, default="line_test")

#     place = models.ForeignKey(Place, on_delete=models.CASCADE)

#     scheduled_time = models.DateTimeField(default=datetime.now())
#     order = models.PositiveIntegerField(default=1)

#     class Meta:
#         ordering = ['order']
#         unique_together = ('bus_line', 'order')

#     def __str__(self):
#         return f"{self.place} at {self.scheduled_time}"
