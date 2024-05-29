# System import.
import uuid

# Django import.
from django.db import models
from django.utils import timezone

class Driver(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='driver', primary_key=True)
    def __str__(self):
        return f"Driver: {self.user.username} (id: {self.pk})"


class Bus(models.Model):
    licence_plate = models.CharField("Name of the bus", max_length=10)
    class Meta:
        verbose_name_plural = "Buses"

    def __str__(self):
        return f"Bus: {self.licence_plate} (id: {self.pk})"

class BusStop(models.Model):
    uid = models.UUIDField(primary_key=True,  default=uuid.uuid4, editable=False)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    time_stop = models.DateTimeField(default=timezone.now, unique=True)
    date = models.DateField(default=None, blank=True, null=True)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.time_stop.strftime("%H:%M:%S")}'

class BusShift(models.Model):
    uid = models.UUIDField(primary_key=True,  default=uuid.uuid4, editable=False)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    bus_stop = models.ForeignKey(BusStop, on_delete=models.CASCADE, blank=True, null=True, related_name='stops')
    departure = models.DateTimeField(editable=False, blank=True, null=True)
    arrival = models.DateTimeField(editable=False, blank=True, null=True)
    travel_time = models.CharField(max_length=50, editable=False, blank=True, null=True)
    date = models.DateField(default=None, blank=True, null=True)
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.uid.hex
    
