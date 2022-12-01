from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from padam_django.apps.fleet.models import Bus, Driver
from padam_django.apps.geography.models import Place


__all__ = ['BusShift', 'BusStop']


class BusShift(models.Model):

    class Meta:
        verbose_name = "Bus shift"
        verbose_name_plural = "Buses shifts"

    bus = models.ForeignKey(
        Bus, models.CASCADE, verbose_name="bus", related_name='shifts')
    driver = models.ForeignKey(
        Driver, models.CASCADE, verbose_name="driver", related_name='shifts')

    def __str__(self):
        return "Bus shift : {} - {} (id: {})".format(
            self.licence_plate, self.driver.user, self.pk)

    @property
    def licence_plate(self):
        return self.bus.licence_plate

    @property
    def start_date(self):
        if not hasattr(self, 'stops'):
            return None
        return self.stops.first().start_date

    @property
    def end_date(self):
        if not hasattr(self, 'stops'):
            return None
        return self.stops.last().end_date

    @property
    def shift_time(self):
        if not hasattr(self, 'stops'):
            return None
        return self.end_date - self.start_date

    @property
    def stops_count(self):
        if not hasattr(self, 'stops'):
            return 0
        return self.stops.count()


class BusStop(models.Model):

    class Meta:
        verbose_name = "Bus stop"
        verbose_name_plural = "Buses stop"

    place = models.ForeignKey(
        Place, models.CASCADE, verbose_name="bus stop", blank=True)
    start_date = models.DateTimeField(verbose_name="start date")
    end_date = models.DateTimeField(verbose_name='end date')
    bus_shift = models.ForeignKey(
        BusShift, models.CASCADE, verbose_name='bus shift', related_name='stops'
    )

    def __str__(self):
        return "Bus stop: {} {} - {} (id: {})".format(
            self.bus_shift.licence_plate, self.place.name,
            self.start_date, self.pk)

    def clean(self):
        super().clean()
        # If end_date > self.start_date & start_date < self.end_date
        # If end_date > self.start_date & start_date < self.end_date
        if self.start_date > self.end_date:
            raise ValidationError(
                "end date must be grather than start date on bus stop")
        stops = self.bus_shift.stops.filter(
            Q(end_date__gte=self.start_date, start_date__lte=self.end_date) |
            Q(end_date__lte=self.start_date, start_date__gte=self.end_date)
        )
        # If entry already exists -> exclude this instance
        if self.pk:
            stops = stops.exclude(pk=self.pk)
        if stops.exists():
            raise ValidationError(
                "Start date must be greater than the previous dates"
            )
