from django.db import models


class Place(models.Model):
    name = models.CharField("Name of the place", max_length=50)

    longitude = models.DecimalField("Longitude", max_digits=9, decimal_places=6)
    latitude = models.DecimalField("Latitude", max_digits=9, decimal_places=6)

    class Meta:
        # Two places cannot be located at the same coordinates.
        unique_together = (("longitude", "latitude"), )

    def __str__(self):
        return f"Place: {self.name} (id: {self.pk})"


class BusStop(models.Model):
    place = models.ForeignKey(to='geography.Place', on_delete=models.PROTECT, related_name='bus_stop')
    pickup_time = models.DateTimeField(verbose_name="Time to reach bus stop", null=False)
    passenger_number = models.IntegerField(verbose_name="Number of passenger to pickup")
    bus_shift = models.ForeignKey(to='journey.BusShift', on_delete=models.CASCADE, related_name='bus_stop',
                                  verbose_name="Bus shift linked to")

    class Meta:
        # Cannot have two bus stops with the same pickup time and bus shift
        unique_together = (("pickup_time", "bus_shift"), )

    def __str__(self):
        return f"BusStop: {self.place.name} at {self.pickup_time} (id: {self.pk})"
