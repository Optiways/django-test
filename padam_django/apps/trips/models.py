from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta


class BusStop(models.Model):
    """
    Represents a bus stop with a specific place, stop time, and unique identifier (name).

    Attributes:
        name (str): The name of the bus stop.
        place (ForeignKey): The geographical location of the stop.
        stop_time (DateTimeField): The scheduled stop time at this place.

    Meta:
        constraints: Ensures that a unique combination of name, place, and stop_time exists.
        ordering: Orders bus stops by their stop time by default.
    """

    name = models.CharField(max_length=100)
    place = models.ForeignKey(
        "geography.Place", on_delete=models.CASCADE, related_name="bus_stops"
    )
    stop_time = models.DateTimeField("Stop Time")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "place", "stop_time"],
                name="unique_place_stop_time",
            )
        ]
        ordering = ["stop_time"]

    def __str__(self):
        return f"{self.place} at {self.stop_time}"


class BusShift(models.Model):
    """
    Represents a shift for a specific bus and driver with assigned stops, start and end times, and a duration.

    Attributes:
        bus (ForeignKey): The bus assigned to this shift.
        driver (ForeignKey): The driver assigned to this shift.
        stops (ManyToManyField): The sequence of bus stops for the shift.
        duration (DurationField): Calculated total duration of the shift.
        start_time (DateTimeField): Calculated start time of the shift.
        end_time (DateTimeField): Calculated end time of the shift.

    Methods:
        clean(): Validates the shift before saving, ensuring unique times, at least two stops, and non-overlapping times.
        _calculate_shift_times(): Sets start_time, end_time, and duration based on stops.
        _validate_unique_shift(): Validates the shift does not overlap with another for the same bus or driver.
        _validate_minimal_busstops_number(): Ensures a minimum of two stops are assigned.
        save(): Overrides save to include validations before saving.
    """

    bus = models.ForeignKey(
        "fleet.Bus", on_delete=models.CASCADE, related_name="shifts"
    )
    driver = models.ForeignKey(
        "fleet.Driver", on_delete=models.CASCADE, related_name="shifts"
    )
    stops = models.ManyToManyField("BusStop")
    duration = models.DurationField("Duration", null=True, blank=True, editable=False)
    start_time = models.DateTimeField(
        "Start Time", null=True, blank=True, editable=False
    )
    end_time = models.DateTimeField("End Time", null=True, blank=True, editable=False)

    def __str__(self):
        return f"Bus shift with Bus {self.bus} and driver {self.driver}"
