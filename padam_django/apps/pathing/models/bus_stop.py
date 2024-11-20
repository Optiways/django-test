from django.core.exceptions import ValidationError
from django.db import models

from padam_django.apps.geography.models import Place
from padam_django.apps.pathing.models.bus_shift import BusShift
from django.utils.timezone import now


class BusStop(models.Model):
    visit_date_time = models.DateTimeField()
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="bus_stops")
    bus_shift = models.ForeignKey(BusShift, on_delete=models.CASCADE, related_name="bus_stops", null=True, blank=True)

    def clean(self):
        super().clean()

        if self.visit_date_time and self.visit_date_time <= now():
            raise ValidationError("The visit date and time can't be in the past.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Bus Stop"
        verbose_name_plural = "Bus Stops"

    def __str__(self):
        return f"{self.visit_date_time} - {self.place}"