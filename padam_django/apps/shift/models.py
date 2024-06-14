import uuid

from django.db import models


class BusStop(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField("Name of the bus stop", max_length=20)
    place = models.ForeignKey("geography.place", on_delete=models.PROTECT)

    def __str__(self):
        return f"Name: {self.name} (id: {self.pk})"


class BusShift(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bus = models.ForeignKey("fleet.bus", on_delete=models.PROTECT)
    driver = models.ForeignKey("fleet.driver", on_delete=models.PROTECT)
    first_stop = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )  # Use this fields as "cache"
    last_stop = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True
    )  # Use this fields as "cache"

    @property
    def shift_duration(self):
        return self.last_stop - self.first_stop

    def __str__(self):
        return f"Bus: {self.bus.licence_plate} driver: {self.driver.user.username} (id: {self.pk})"


class ScheduleStop(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bus_shift = models.ForeignKey(BusShift, on_delete=models.PROTECT)
    bus_stop = models.ForeignKey(BusStop, on_delete=models.PROTECT)
    arrival = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return f"Shift: {self.bus_shift} stop: {self.bus_stop.name} (id: {self.pk})"
