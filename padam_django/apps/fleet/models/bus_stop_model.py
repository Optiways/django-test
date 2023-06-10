from django.db import models


class BusStop(models.Model):
    place = models.OneToOneField(
        "geography.Place", on_delete=models.CASCADE, related_name="place"
    )
    stop_time = models.DateTimeField(verbose_name="Bus stop datetime")

    def __str__(self):
        return f"BusStop: {self.place} the {self.stop_time.date()} at {self.stop_time.time()} (id: {self.pk})"
