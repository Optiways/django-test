from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError
from padam_django.apps.geography.models import Place
from padam_django.apps.fleet.models import Bus, Driver


class BusStop(models.Model):
    name = models.CharField(
        verbose_name="Name of the bus stop",
        max_length=100,
    )
    is_transfer_stop = models.BooleanField(
        verbose_name="Transfer stop", default=False,
    )
    location = models.ForeignKey(
        Place,
        verbose_name="Location",
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name="stops",
    )

    def __str__(self):
        return f"Bus stop: {self.name}"


class BusStopTime(models.Model):
    transit_time = models.TimeField(
        verbose_name="Time of transit", null=False, blank=False
    )
    stop = models.ForeignKey(
        BusStop,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"Bus stop in {self.stop.name} at {self.transit_time}"


class BusShift(models.Model):
    departure_stop = models.ForeignKey(
        BusStopTime,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name="shifts_departure",
    )
    arrival_stop = models.ForeignKey(
        BusStopTime,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name="shifts_arrival",
    )
    driver = models.ForeignKey(
        Driver,
        verbose_name="Driver",
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name="shifts_driver",
    )

    bus = models.ForeignKey(
        Bus,
        verbose_name="Bus",
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name="shifts_bus",
    )

    bus_stops = models.ManyToManyField(
        BusStop, related_name="shifts_stop", blank=True,
    )

    @property
    def count_bus_stops(self):
        return self.bus_stops.count()

    def total_shift_time(self):
        departure = self.departure_stop.transit_time
        arrival = self.arrival_stop.transit_time
        elapse_time = datetime.strptime(
            arrival, "%H:%M:%S"
        ) - datetime.strptime(departure, "%H:%M:%S")

        return round(elapse_time.total_seconds() / 60)

    @property
    def departure_stop_name(self):
        return self.departure_stop.stop.name

    @property
    def arrival_stop_name(self):
        return self.arrival_stop.stop.name

    def clean(self):
        from .utils import check_overlap

        if self.arrival_stop.transit_time <= self.departure_stop.transit_time:
            raise ValidationError(
                "Arrival time cannot be equal or before departure time"
            )

        driver = Driver.objects.get(pk=self.driver.pk)
        driver_shifts = driver.shifts_driver.all()
        bus = Bus.objects.get(pk=self.bus.pk)
        bus_shifts = bus.shifts_bus.all()

        if check_overlap(self, driver_shifts):
            raise ValidationError("Driver already assigned")

        if check_overlap(self, bus_shifts):
            raise ValidationError("Bus already assigned")

    def __str__(self):
        return (
            "Bus shift:"
            f" {self.driver} {self.departure_stop.transit_time}"
            f"-{self.arrival_stop.transit_time}"
        )
