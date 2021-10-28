from django.db import models

from padam_django.apps.geography.models import Place


class Driver(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='driver')

    def __str__(self):
        return f"Driver: {self.user.username} (id: {self.pk})"


class Bus(models.Model):
    licence_place = models.CharField("Name of the bus", max_length=10)

    class Meta:
        verbose_name_plural = "Buses"

    def __str__(self):
        return f"Bus: {self.licence_place} (id: {self.pk})"


class BusShift(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    bus_stops = models.ManyToManyField("BusStop")

    departure = models.DateTimeField()
    arrival = models.DateTimeField()

    # Constraint Check if instance of shift has bus/driver and is not in timetable of departure/arrival of another
    #   instance, UniqueConstraint doesnt stop from creating instances without the necessary constraints
    class Meta:
        # constraint = [
        #     models.CheckConstraint(check=models.Q)
        # ]
        models.UniqueConstraint(fields=['bus', 'departure', 'arrival'], name='unique_bus_booking')
        models.UniqueConstraint(fields=['driver', 'departure', 'arrival'], name='unique_driver_booking')

    def __str__(self):
        return f"Time Table: {self.departure} - {self.arrival} (id: {self.pk})"


class BusStop(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)

    # Need to figure out how to obtain name
    # def __str__(self):
    #     return f"Place: (id: {self.pk})"
