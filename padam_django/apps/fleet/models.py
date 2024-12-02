from django.db import models
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


class BusStop(models.Model):
    place = models.ForeignKey(Place, verbose_name="Place", on_delete=models.CASCADE)
    time = models.DateTimeField(verbose_name="Time")

    class Meta:
        verbose_name = "Bus stop"
        verbose_name_plural = "Bus stops"
        ordering = ["time"]

    def __str__(self):
        return f"Bus stop: {self.place} - time: {self.time}"


class BusShift(models.Model):
    bus = models.ForeignKey(Bus, verbose_name="Bus", on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, verbose_name="Driver", on_delete=models.CASCADE)
    bus_stop = models.ManyToManyField(BusStop)
    start_dt = models.DateTimeField(verbose_name="Beginning of the trip")
    end_dt = models.DateTimeField(verbose_name="End of the trip")

    class Meta:
        verbose_name = "Bus shift"
        verbose_name_plural = "Bus shifts"

    def __str__(self):
        return f"Bus_shift: {self.bus} - {self.driver}"

    @property
    def duration(self):
        return self.end_dt - self.start_dt
