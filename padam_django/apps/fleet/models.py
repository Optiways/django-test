from django.db import models

from padam_django.apps.fleet.services import get_time_diff_between


class Driver(models.Model):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE, related_name="driver")

    def __str__(self):
        return f"Driver: {self.user.username} (id: {self.pk})"


class Bus(models.Model):
    licence_plate = models.CharField("Name of the bus", max_length=10)

    class Meta:
        verbose_name_plural = "Buses"

    def __str__(self):
        return f"Bus: {self.licence_plate} (id: {self.pk})"


class BusStop(models.Model):
    place = models.ForeignKey("geography.Place", on_delete=models.CASCADE)
    departure_time = models.TimeField()
    bus = models.ForeignKey(
        "fleet.Bus", null=True, blank=True, related_name="stops", on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"Bus Stop: {self.place.name} (id: {self.pk})"

    class Meta:
        ordering = ["departure_time"]


class BusShift(models.Model):
    bus = models.ForeignKey("fleet.Bus", on_delete=models.CASCADE, related_name="shifts")
    driver = models.ForeignKey("fleet.Driver", on_delete=models.CASCADE, related_name="shifts")
    stops = models.ManyToManyField("fleet.BusStop", related_name="shifts")
    departure_time = models.TimeField()
    arrival_time = models.TimeField()

    @property
    def duration(self) -> str:
        hours, minutes = get_time_diff_between(self.departure_time, self.arrival_time)
        return f"{hours:02d}h{minutes:02d}"

    def __str__(self):
        return f"Bus Shift: {self.driver.user} - {self.bus.licence_plate} - {self.duration} (id: {self.pk})"
