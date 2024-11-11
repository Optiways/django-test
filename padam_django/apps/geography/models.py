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
    """
    A bus stop is a Place where a bus is expected to stop at a given time.
    """
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    expected_arrival = models.TimeField("Expected arrival time")

    class Meta:
        # A bus stop cannot be duplicated.
        # its either same time different place or same place different time
        unique_together = (("place", "expected_arrival"),)

    def __str__(self):
        return f"BusStop: {self.place.name} at {self.expected_arrival}"
