import datetime
from django.db import models
from django.forms import ValidationError
from padam_django.apps.geography.models import Place


class Driver(models.Model):
    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="driver"
    )

    def __str__(self):
        return f"Driver: {self.user.username} (id: {self.pk})"


class Bus(models.Model):
    licence_plate = models.CharField("Name of the bus", max_length=10)

    class Meta:
        verbose_name_plural = "Buses"

    def __str__(self):
        return f"Bus: {self.licence_plate} (id: {self.pk})"


class BusShift(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.RESTRICT)
    driver = models.ForeignKey(Driver, on_delete=models.RESTRICT)

    @property
    def start(self) -> "BusStop":
        return BusStop.objects.filter(shift=self.pk).earliest("time")

    @property
    def end(self) -> "BusStop":
        return BusStop.objects.filter(shift=self.pk).latest("time")

    @property
    def duration(self) -> datetime.timedelta:
        return self.end.time - self.start.time

    @property
    def number_of_stops(self) -> int:
        return BusStop.objects.filter(shift=self.pk).count()

    def __str__(self) -> str:
        return f"Shift from {self.start.place} to {self.end.place} ({self.pk})"

    def clean(self):
        if self.number_of_stops < 2:
            raise ValidationError("Shift need at least 2 stops")


class BusStop(models.Model):
    place = models.ForeignKey(Place, on_delete=models.RESTRICT)
    time = models.DateTimeField()
    shift = models.ForeignKey(BusShift, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.place} at {self.time} ({self.pk})"
