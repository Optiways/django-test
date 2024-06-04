from django.core.exceptions import ValidationError
from django.db import models

from ..geography.models import Place


class Driver(models.Model):
    """
    Model representing a driver.

    Attributes:
        user (OneToOneField): The user associated with the driver.
    """

    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="driver"
    )

    def __str__(self):
        """
        Returns a string representation of the driver.
        """
        return f"Driver: {self.user.username} (id: {self.pk})"


class Bus(models.Model):
    """
    Model representing a bus.

    Attributes:
        licence_plate (CharField): The licence plate of the bus.
    """

    licence_plate = models.CharField("Name of the bus", max_length=10)

    class Meta:
        verbose_name_plural = "Buses"

    def __str__(self):
        """
        Returns a string representation of the bus.
        """
        return f"Bus: {self.licence_plate} (id: {self.pk})"


class BusStop(models.Model):
    """
    Model representing a bus stop.

    Attributes:
        name (CharField): The name of the bus stop.
        place (ForeignKey): The place associated with the bus stop.
        departure_time (DateTimeField): The departure time of the bus stop.
        arrival_time (DateTimeField): The arrival time of the bus stop.
    """

    name = models.CharField(max_length=100)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    departure_time = models.DateTimeField(blank=True, null=True)
    arrival_time = models.DateTimeField(blank=True, null=True)

    def clean(self):
        """
        Validates that either arrival time or departure time is provided.
        """
        if self.arrival_time is None and self.departure_time is None:
            raise ValidationError(
                "Either Arrival time or Departure time must be provided."
            )

    def __str__(self):
        """
        Returns a string representation of the bus stop.
        """
        return self.name


class BusShift(models.Model):
    """
    Model representing a bus shift.

    Attributes:
        bus (ForeignKey): The bus associated with the bus shift.
        driver (ForeignKey): The driver associated with the bus shift.
        stops (ManyToManyField): The stops associated with the bus shift.
    """

    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    stops = models.ManyToManyField(BusStop, related_name="bus_shifts")

    @property
    def start_time(self):
        """
        Calculates the start time of the bus shift.
        """
        first_stop = (
            self.stops.exclude(departure_time__isnull=True)
            .order_by("departure_time")
            .first()
        )
        return first_stop.departure_time if first_stop else None

    @property
    def end_time(self):
        """
        Calculates the end time of the bus shift.
        """
        last_stop = (
            self.stops.exclude(arrival_time__isnull=True)
            .order_by("arrival_time")
            .last()
        )
        return last_stop.arrival_time if last_stop else None

    @property
    def total_duration(self):
        """
        Calculates the total duration of the bus shift.
        """
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            return duration
        return None

    def __str__(self):
        """
        Returns a string representation of the bus shift.
        """
        return f"BusShift: {self.bus.licence_plate} (id: {self.pk})"
