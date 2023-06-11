from django.db import models


class BusStop(models.Model):
    place = models.ForeignKey(
        "geography.Place", on_delete=models.CASCADE, related_name="stops"
    )
    datetime = models.DateTimeField(verbose_name="Bus stop datetime")
    shift = models.ForeignKey(
        "fleet.BusShift", on_delete=models.CASCADE, related_name="stops"
    )

    def __str__(self):
        return f"BusStop: {self.place} the {self.datetime.date()} at {self.datetime.time()} (id: {self.pk})"
