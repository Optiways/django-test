from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import datetime

class BusStop(models.Model):
    """
    Bus stop : defined by a place and a time
    """

    place = models.ForeignKey('geography.Place', on_delete=models.CASCADE, related_name='place')
    time = models.TimeField()

    def __str__(self):
        return f"Bus Stop: {self.place} - {self.time} (id: {self.pk})"

class BusShift(models.Model):
    """
    Bus shift : defined by a bus, his driver, a starting bus stop and a last bus stop
    optional : intermediate bus stop(s)
    """

    bus = models.ForeignKey('fleet.Bus', on_delete=models.CASCADE, related_name='bus')
    driver = models.ForeignKey('fleet.Driver', on_delete=models.CASCADE, related_name='driver')
    start = models.ForeignKey(BusStop, on_delete=models.CASCADE, related_name='start')
    end = models.ForeignKey(BusStop, on_delete=models.CASCADE, related_name='end')
    steps = models.ManyToManyField(BusStop, blank=True)

    @property
    def driving_time(self):
        """
        Return the total time of the route
        """
        t1 = self.start.time
        t2 = self.end.time
        return t2 - t1

    def clean(self):
        """
        Input constraints :
        - starting bus stop time before ending bus stop time
        - steps are between starting and ending times
        - the bus is available
        - the driver is available
        """
        if self.start.time > self.end.time:
            raise ValidationError(
                {"end": "Ending bus stop time must be later than starting bus stop time"}
            )


        query = BusShift.objects.filter(driver=self.driver, start__time__range=[self.start.time, self.end.time]) | BusShift.objects.filter(driver=self.driver, end__time__range=[self.start.time, self.end.time]) | BusShift.objects.filter(driver=self.driver, start__time__lte=self.start.time, end__time__gte=self.end.time)
        if self.id:
            query = query.exclude(id=self.id)
        if query.exists():
            raise ValidationError(
                {"driver": "Choosen driver is not available during selected time range"}
            )

        query = BusShift.objects.filter(bus=self.bus, start__time__range=[self.start.time, self.end.time]) | BusShift.objects.filter(bus=self.bus, end__time__range=[self.start.time, self.end.time]) | BusShift.objects.filter(bus=self.bus, start__time__lte=self.start.time, end__time__gte=self.end.time)
        if self.id:
            query = query.exclude(pk=self.id)
        if query.exists():
            raise ValidationError(
                {"bus": "Choosen bus is not available during selected time range"}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Bus Shift: from {self.start.place} to {self.end.place} - {self.bus} - {self.driver}"