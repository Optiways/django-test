from django.db import models
from django.forms import ValidationError
from django.utils.translation import ugettext_lazy as _


class Driver(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='driver')

    def __str__(self):
        return f"Driver: {self.user.username}"
        # return f"Driver: {self.user.username} (id: {self.pk})"


class Bus(models.Model):
    licence_plate = models.CharField("Name of the bus", max_length=10)

    class Meta:
        verbose_name_plural = "Buses"

    def __str__(self):
        return f"Bus: {self.licence_plate}"
        # return f"Bus: {self.licence_plate} (id: {self.pk})"


class BusStop(models.Model):
    pass_time = models.DateTimeField(null=False)
    place = models.ForeignKey('geography.Place', on_delete=models.CASCADE, related_name="bus_stops")

    def __str__(self):
        return f"{self.place} -- {self.pass_time}"
        # return f"BusStop: [{self.place}, at {self.pass_time}]"

    class Meta:
        ordering = ['-pass_time']

class BusShift(models.Model):
    driver = models.ForeignKey("fleet.Driver", verbose_name=_("Drivers"), on_delete=models.CASCADE, related_name="bus_shifts")
    bus = models.ForeignKey(Bus, verbose_name=_("bus"), on_delete=models.CASCADE, related_name="bus_shifts")
    departure = models.ForeignKey(BusStop, verbose_name=_("Departure"), on_delete=models.CASCADE, related_name="+")
    arrival = models.ForeignKey(BusStop, verbose_name=_("Arrival"), on_delete=models.CASCADE, related_name="+")
    bus_stops = models.ManyToManyField(BusStop, verbose_name="Bus Stops", related_name="bus_shifts", blank=True)

    class Meta:
        verbose_name_plural = "Buses Shifts"
        verbose_name = "Bus Shift"
        unique_together = (
            ("departure", "arrival", "bus", "driver"),
        )

    def __str__(self):
        # return f"BusShift (id: {self.pk}): {self.bus.licence_plate} from {self.departure.place} to {self.arrival.place}"
        return f"BusShift (id: {self.pk})"

    def clean(self):
        # we need to check depart < arrival time
        # we need to check if all busStop are odred and their pass_time is between depart, arrival
        if self.id:
            queryset = self.bus_stops.order_by('pass_time')
            if queryset.count() > 0:
                if queryset.first().pass_time < self.departure.pass_time:
                    raise ValidationError([{
                        "departure": "invalid departure BusStop!"
                    }])
                if queryset.last().pass_time > self.arrival.pass_time:
                    raise ValidationError([{
                        "arrival": "invalid arrival BusStop!"
                    }])
        return super().clean()
