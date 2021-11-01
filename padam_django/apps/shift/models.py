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
        verbose_name="Time of transit",
        null=False,
        blank=False,
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

    departure_time = models.ForeignKey(
        BusStopTime,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name="shifts_departure",
    )
    arrival_time = models.ForeignKey(
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
        BusStop, related_name="shifts_stop", blank=False,
        help_text="Select at least 2 bus stops",
    )

    def total_shift_time(self):
        """Travel time in minutes"""
        departure = self.departure_time.transit_time
        arrival = self.arrival_time.transit_time

        elapse_time = datetime.strptime(
            arrival, "%H:%M:%S"
        ) - datetime.strptime(departure, "%H:%M:%S")

        return round(elapse_time.total_seconds() / 60)

    @property
    def departure_stop_name(self):
        return self.departure_time.stop.name

    @property
    def arrival_stop_name(self):
        return self.arrival_time.stop.name

    def clean(self):
        """Validate data"""

        from .utils import check_overlap

        if not all(hasattr(self, attr) for attr in ["arrival_time", "departure_time", "driver", "bus"]):
            raise ValidationError("All fields must be filled")

        if self.arrival_time.transit_time <= self.departure_time.transit_time:
            raise ValidationError(
                "Arrival time cannot be equal or before departure time."
            )

        driver_shifts = self.driver.shifts_driver.exclude(pk=self.id)
        bus_shifts = self.bus.shifts_bus.exclude(pk=self.id)

        if check_overlap(self.departure_time.transit_time,
                         self.arrival_time.transit_time, driver_shifts):
            raise ValidationError("Driver is already assigned.")

        if check_overlap(self.departure_time.transit_time,
                         self.arrival_time.transit_time, bus_shifts):
            raise ValidationError("Bus is already assigned.")

    def __str__(self):
        return (
            "Bus shift:"
            f" {self.driver.user.username} {self.departure_time.transit_time}"
            f"-{self.arrival_time.transit_time}"
        )
