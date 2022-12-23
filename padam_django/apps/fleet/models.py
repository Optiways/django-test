from __future__ import annotations

import datetime

import django
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property


class Driver(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='driver')

    def __str__(self):
        return f"Driver: {self.user.username} (id: {self.pk})"


class Bus(models.Model):
    licence_plate = models.CharField("Name of the bus", max_length=10)

    class Meta:
        verbose_name_plural = "Buses"

    def __str__(self):
        return f"Bus: {self.licence_plate} (id: {self.pk})"


class BusShift(models.Model):
    """
    Management model for bus shifting, related to :model:`fleet.Bus`, :model:`fleet.Driver`, :model:`fleet.BusStop`.
    :param bus: bus used for the shift
    :param driver: driver assigned to the shift
    :param stops: list of stops of shift
    """
    bus = models.ForeignKey('fleet.Bus', on_delete=models.CASCADE, null=False, related_name='bus_shift')
    driver = models.ForeignKey('fleet.Driver', on_delete=models.CASCADE, null=False, related_name='bus_shift')
    stops = models.ManyToManyField('fleet.BusStop', related_name='bus_shift',
                                   help_text="list of all stops during shift")

    class Meta:
        verbose_name_plural = "Buses Shifts"

    def __str__(self) -> str:
        return f"Bus shift id: {self.pk}"

    @cached_property
    def arrival_date(self) -> datetime:
        """return the date of passage to the last stop"""
        return max(self.get_stops.values_list('schedule'))[0] if self.stops else None

    @cached_property
    def departure_date(self) -> datetime:
        """return the date of passage to the first stop"""
        return min(self.get_stops.values_list('schedule'))[0] if self.stops else None

    @cached_property
    def get_stops(self) -> list[BusStop]:
        """return list of all the stops for the shift"""
        return self.stops.all()

    @cached_property
    def stops_count(self) -> int:
        """return count of stops for the shit"""
        return self.stops.count()

    @cached_property
    def travel_time(self) -> datetime:
        """return shift duration"""
        return self.arrival_date - self.departure_date

    def get_absolute_url(self):
        return reverse("fleet:bus_shift", kwargs={'pk': self.pk})

    # def save(self) -> Union[ValidationError, None]:
    #     super().save()
    #     errors: dict[str, str] = {}
    #     # validate bus availability for the shift
    #     stored_bus_shift: QuerySet = self.bus.bus_shift.all()
    #     if stored_bus_shift:
    #         for shift in stored_bus_shift:
    #             if shift.pk != self.pk and shift.departure_date >= self.departure_date and shift.arrival_date <= self.arrival_date:
    #                 errors["bus"] = "This bus is already affected to another shift during this period"
    #                 break
    #     # validate driver availability for the shift
    #     stored_driver_shift: QuerySet = self.driver.bus_shift.all()
    #     if stored_driver_shift:
    #         for shift in stored_driver_shift:
    #             if shift.pk != self.pk and shift.departure_date >= self.departure_date and shift.arrival_date <= self.arrival_date:
    #                 errors["driver"] = "This driver is already affected to another shift during this period"
    #                 break
    #     # # validate minimal shift length
    #     # if self.stops_count < 2:
    #     #     errors["stops"] = "Bus Shift must have at least 2 stops"
    #     if errors:
    #         raise ValidationError(errors)


class BusStop(models.Model):
    """
    Management model for bus stop planification to :model:`'geography.Place`.
    :param place: geographic location
    :param schedule: date shift possible
    """
    place = models.ForeignKey('geography.Place', on_delete=models.CASCADE, null=False, related_name='bus_stop')
    schedule = models.DateTimeField(default=django.utils.timezone.now, null=False)

    class Meta:
        verbose_name_plural = "Buses Stops"

    def __str__(self):
        return f"Bus stop: {self.place.name} {self.schedule} (id: {self.pk})"
