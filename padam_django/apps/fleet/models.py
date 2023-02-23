from typing import Optional
from django.db import models
from django.core.exceptions import ValidationError


class Driver(models.Model):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE, related_name="driver")

    def __str__(self):
        return f"{self.user.username} (id: {self.pk})"


class Bus(models.Model):
    licence_plate = models.CharField("Name of the bus", max_length=10)

    class Meta:
        verbose_name_plural = "Buses"

    def __str__(self):
        return f"{self.licence_plate} (id: {self.pk})"


class BusStop(models.Model):
    place = models.ForeignKey("geography.Place", on_delete=models.CASCADE)
    departure_time = models.TimeField()
    bus = models.ForeignKey(
        "fleet.Bus", null=True, blank=True, related_name="stops", on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.place.name} (id: {self.pk})"

    class Meta:
        ordering = ["departure_time"]


class BusShift(models.Model):
    bus = models.ForeignKey("fleet.Bus", on_delete=models.CASCADE, related_name="shifts")
    driver = models.ForeignKey("fleet.Driver", on_delete=models.CASCADE, related_name="shifts")
    stops = models.ManyToManyField("fleet.BusStop", related_name="shifts")
    departure_time = models.TimeField(null=True, blank=True)
    arrival_time = models.TimeField(null=True, blank=True)

    @property
    def duration(self) -> Optional[str]:
        """Get shift duration in hours:minutes"""
        # TODO: Fix Circular import between services - models, need to check it
        from padam_django.apps.fleet.services import get_time_diff_between
        if not self.departure_time or not self.arrival_time:
            return None
        hours, minutes = get_time_diff_between(self.departure_time, self.arrival_time)
        return f"{hours:02d}h{minutes:02d}"

    def save(self, *args, **kwargs) -> None:
        """Check for bus and driver availability if departure_time and arrival_time is defined
        :raise ValidationError in case of bus or driver has already a shift at this time

        TODO: Refacto check_x_availability services to respect Single Responsability principle
        """
        from padam_django.apps.fleet.services import (
            check_bus_availability,
            check_driver_availability,
        )
        if not self.departure_time or not self.arrival_time:
            super(BusShift, self).save(*args, **kwargs)
            return

        bus_is_available = check_bus_availability(self.bus, self.departure_time, self.arrival_time, self.pk)
        if bus_is_available is False:
            raise ValidationError("The bus is already assigned to a trip at the same time.")

        driver_is_available = check_driver_availability(
            self.driver, self.departure_time, self.arrival_time, self.pk
        )
        if driver_is_available is False:
            raise ValidationError("The driver is already assigned to a trip at the same time.")

        super(BusShift, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.driver.user} - {self.bus.licence_plate} - {self.duration} (id: {self.pk})"
