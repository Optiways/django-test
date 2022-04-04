from django.db import models

from padam_django.apps.fleet.models import Bus, Driver
from padam_django.apps.geography.models import Place


class BusShift(models.Model):
    """
    Elements integrating a bus trip that can have multiple bus stops.
    """
    bus = models.ForeignKey("fleet.Bus", on_delete=models.CASCADE)
    driver = models.ForeignKey("fleet.Driver", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "bus shifts"
        constraints = [
            models.UniqueConstraint(
                fields=["bus", "driver"], name="unique_driver_bus"
            ),
        ]


class BusStop(models.Model):
    """
    Basic unit of a reservation having a starting and an ending point. 
    
    This model has the 'a priori' assumption that the person that generates 
    a bus stop knows the estimated time to get from the starting point to the 
    ending point.
    """
    bus_shift =  models.ForeignKey("BusShift", on_delete=models.CASCADE)
    start_point = models.ForeignKey(
        "geography.Place", on_delete=models.CASCADE, related_name="departure" 
    )
    end_point = models.ForeignKey(
        "geography.Place", on_delete=models.CASCADE, related_name="arrival"
    )
    start_time = models.DateTimeField(
        verbose_name="Time of departure", null=False
    )
    end_time = models.DateTimeField(
        verbose_name="Time of arrival", null=False
    )

    class Meta:
        verbose_name_plural = "bus stops"
        constraints = [
            models.UniqueConstraint(
                fields=["bus_shift", "start_time"], name="specific_stop"
            ),
            models.CheckConstraint(
                check=models.Q(end_time__gt=models.F("start_time")), 
                name="coherent_time"
            )
        ]
        ordering = ("-end_time", )