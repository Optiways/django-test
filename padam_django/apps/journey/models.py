import pytz

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, Max, Min

from padam_django.apps.fleet.models import Bus, Driver
from padam_django.apps.geography.models import Place


class BusShift(models.Model):

    bus = models.ForeignKey(Bus, on_delete=models.deletion.PROTECT)
    driver = models.ForeignKey(Driver, on_delete=models.deletion.PROTECT)

    def __str__(self):
        return f"BusShift: {self.bus} {self.driver} (id: {self.pk})"


class BusStop(models.Model):

    datetime = models.DateTimeField()
    place = models.ForeignKey(Place, on_delete=models.deletion.PROTECT)
    bus_shift = models.ForeignKey(BusShift, on_delete=models.deletion.CASCADE)

    def get_overlappings(self, start_datetime, stop_datetime):
        return (
            BusStop.objects.values("bus_shift_id")
            .annotate(start_datetime=Min("datetime"), stop_datetime=Max("datetime"))
            .filter(
                ~Q(bus_shift__id=self.bus_shift_id),
                start_datetime__lt=stop_datetime,
                stop_datetime__gt=start_datetime,
            )
        )

    def get_bus_overlappings(self, start_datetime, stop_datetime):
        overlappings = self.get_overlappings(start_datetime, stop_datetime)
        return overlappings.filter(bus_shift__bus__id=self.bus_shift.bus_id)

    def get_driver_overlappings(self, start_datetime, stop_datetime):
        overlappings = self.get_overlappings(start_datetime, stop_datetime)
        return overlappings.filter(bus_shift__driver__id=self.bus_shift.driver_id)

    def clean(self):

        tzinfo = pytz.timezone(settings.TIME_ZONE)
        aware_datetime = self.datetime.replace(tzinfo=tzinfo)
        start_datetime = stop_datetime = aware_datetime

        other_bus_stops = (
            BusStop.objects.values("bus_shift_id")
            .annotate(start_datetime=Min("datetime"), stop_datetime=Max("datetime"))
            .filter(bus_shift__id=self.bus_shift_id)
        )

        if other_bus_stops:
            start_datetime = min(start_datetime, other_bus_stops[0]["start_datetime"])
            stop_datetime = max(stop_datetime, other_bus_stops[0]["stop_datetime"])

        if self.get_bus_overlappings(start_datetime, stop_datetime).count():
            raise ValidationError(
                f"The bus is already used some time between {start_datetime} and {stop_datetime}"
            )

        if self.get_driver_overlappings(start_datetime, stop_datetime).count():
            raise ValidationError(
                f"The driver is already busy some time between {start_datetime} and {stop_datetime}"
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"BusStop: {self.bus_shift} {self.datetime} (id: {self.pk})"
