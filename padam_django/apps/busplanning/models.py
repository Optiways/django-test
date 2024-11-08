from django.db import models
from ..fleet.models import Bus, Driver
from ..geography.models import Place


# Create your models here.
class BusStop(models.Model):
    name = models.CharField("Stop name", max_length=63)

    location = models.OneToOneField(
        Place,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Stop name: {self.name} (id: {self.pk})"


class BusShift(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)  # can be null but must raise an error

    bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True)  # can be null but must raise an error

    start_time = models.TimeField("Departure time", null=False)
    end_time = models.TimeField("Arrival time", null=False)


class BusShiftStops(models.Model):
    class Meta:
        db_table = 'bus_shift_stops'
        unique_together = (
            ("shift", "stop"),  # A stop cannot be twice in a same shift/path
            ("shift", "index"),
        )

    shift = models.ForeignKey(
        BusShift,
        on_delete=models.CASCADE
    )
    stop = models.ForeignKey(
        BusStop,
        on_delete=models.CASCADE
    )

    index = models.PositiveIntegerField()  # for ordering purposes
