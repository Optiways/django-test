from django.db import models


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
    """

    bus = models.ForeignKey(
        "fleet.Bus", on_delete=models.CASCADE, related_name="shifts"
    )
    driver = models.ForeignKey(
        "fleet.Driver", on_delete=models.CASCADE, related_name="shifts"
    )
    stops = models.ManyToManyField("BusStop")
    start_time = models.DateTimeField(
        "Start Time", null=True, blank=True, editable=False
    )
    end_time = models.DateTimeField("End Time", null=True, blank=True, editable=False)

    @property
    def duration(self):
        if self.end_time and self.start_time:
            return self.end_time - self.start_time

    def __str__(self):
        return f"Bus shift with Bus {self.bus} and driver {self.driver}"
