from django.db import models
from django.db.models import CheckConstraint, F, Q, UniqueConstraint

from padam_django.apps.fleet.models import Bus, Driver


class BusShift(models.Model):
    """
    Elements integrating a bus trip that can have multiple bus stops.
    """
    bus = models.ForeignKey("fleet.Bus", on_delete=models.CASCADE)
    driver = models.ForeignKey("fleet.Driver", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = ("bus trips")


class BusStop(models.Model):
    """
    Basic unit of a reservation having a starting and an ending point. 
    
    This model has the 'a priori' assumption that the person that generates 
    a bus stop knows the estimated time to get from the starting point to the 
    ending point.
    """
    bus_shift =  models.ForeignKey("BusShift", on_delete=models.CASCADE)
    start_point = models.CharField(max_length=50)
    end_point = models.CharField(max_length=50)
    start_time = models.DateTimeField("Time of departure")
    end_time = models.DateTimeField("Time of arrival")

    class Meta:
        verbose_name_plural = ("bus stops")
        