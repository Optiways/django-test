from datetime import datetime

from django.db import models
from padam_django.apps.transit.models import BusShift, BusStop


class Driver(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='driver')

    def is_available(self, from_time: datetime, to_time: datetime, exclude_id: int = None) -> bool:
        """
            Check if the driver is available from the given time range by checking the overlapping
            between time and shift.
            #TODO : De duplicate the next Query
        """
        return not BusShift.objects.filter(
            driver=self
        ).exclude(id=exclude_id).annotate(
            start=models.Subquery(
                BusStop.objects.filter(bus_shift=models.OuterRef("pk")).order_by("transit_time").values("transit_time")[
                :1]),
            end=models.Subquery(
                BusStop.objects.filter(bus_shift=models.OuterRef("pk")).order_by("-transit_time").values(
                    "transit_time")[:2])
        ).filter(
            models.Q(start__gt=from_time, start__lt=to_time) | models.Q(end__gt=from_time, end__lt=to_time) | models.Q(
                start__lt=from_time, end__gt=to_time)
        ).exists()

    def __str__(self):
        return f"Driver: {self.user.username} (id: {self.pk})"


class Bus(models.Model):
    licence_plate = models.CharField("Name of the bus", max_length=10)

    class Meta:
        verbose_name_plural = "Buses"

    def is_available(self, from_time: datetime, to_time: datetime, exclude_id: int = None) -> bool:
        """
            Check if the bus is available from the given time range by checking the overlapping
            between time and shift.
        """
        return not BusShift.objects.filter(
            bus=self
        ).exclude(id=exclude_id).annotate(
            start=models.Subquery(
                BusStop.objects.filter(bus_shift=models.OuterRef("pk")).order_by("transit_time").values("transit_time")[
                :1]),
            end=models.Subquery(
                BusStop.objects.filter(bus_shift=models.OuterRef("pk")).order_by("-transit_time").values(
                    "transit_time")[:2])
        ).filter(
            models.Q(start__gt=from_time, start__lt=to_time) | models.Q(end__gt=from_time, end__lt=to_time) | models.Q(
                start__lt=from_time, end__gt=to_time)
        ).exists()

    def __str__(self):
        return f"Bus: {self.licence_plate} (id: {self.pk})"
