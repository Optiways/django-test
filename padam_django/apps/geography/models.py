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
    name = models.CharField("Name of Bus Stop", max_length=100)
    # using Place to define Bus Stop location
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="places")
    
    def __str__(self):
        return f"Bus Stop: {self.name} (id: {self.pk})"