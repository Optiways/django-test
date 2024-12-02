from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class BusShift(models.Model):
    bus = models.ForeignKey("fleet.Bus", on_delete=models.PROTECT, related_name="bus_shift")
    driver = models.ForeignKey("fleet.Driver", on_delete=models.PROTECT, related_name="bus_shift")
    departure_time = models.DateTimeField(null=False, blank=False)
    arrival_time = models.DateTimeField(null=False, blank=False)

    def __str__(self) -> str:
        return f"Bus Shift (bus: {self.bus.licence_plate} - driver: {self.driver.user})"

    @property
    def total_route_time(self) -> str:
        """Get the total time necessary to complete the journey"""
        elapsed_time = self.arrival_time - self.departure_time
        total_seconds = elapsed_time.seconds
        hours, minutes, seconds = total_seconds // 3600, (total_seconds % 3600) // 60, (total_seconds % 3600) % 60
        return f"{hours}:{minutes}:{seconds}"

    def is_driver_or_bus_available(self) -> bool:
        """Check if another BusShift would have the same bus and driver whose start and end times overlap"""
        bus_shift_overlapping = BusShift.objects.exclude(pk=self.pk).filter(
            Q(bus=self.bus) | Q(driver=self.driver),
            arrival_time__gte=self.departure_time,
            departure_time__lte=self.arrival_time
        )
        # If an overlapping shift has been found, the driver/bus is not available
        return not bus_shift_overlapping.exists()

    def clean(self):
        super().clean()
        # The same bus or driver cannot be assigned to another BusShift whose start and end times overlap
        if not self.is_driver_or_bus_available():
            raise ValidationError("This bus or driver is already taken on another shift on those times.")


class BusStop(models.Model):
    """A BusStop is a point in time when a bus from a BusShift will pass at this place"""
    place = models.ForeignKey("geography.Place", on_delete=models.CASCADE, related_name="bus_stop")
    bus_shift = models.ForeignKey("BusShift", on_delete=models.PROTECT, related_name="bus_stop")
    passage_time = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return f"Bus Stop at {self.place.name}"
