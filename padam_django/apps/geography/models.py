from padam_django.apps.fleet.models import Driver, Bus
from django.core.exceptions import ValidationError
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
    stop = models.OneToOneField(Place, on_delete=models.CASCADE)

    def __str__(self):
        return f"Bus stop: {self.stop} "


class BusShift(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    stop = models.ManyToManyField(BusStop)
    start_ride = models.DateTimeField()
    stop_ride = models.DateTimeField()

    def save(self, *args, **kwargs):

        # get all the bus shifts whose start or end time is within the time interval of the shift that you want to define
        shifts_already_booked_start = BusShift.objects.filter(start_ride__range=[self.start_ride, self.stop_ride])
        shifts_already_booked_stop = BusShift.objects.filter(stop_ride__range=[self.start_ride, self.stop_ride])
        shifts_booked_at_the_same_time = shifts_already_booked_start | shifts_already_booked_stop

        for shift in shifts_booked_at_the_same_time:
            # TODO : message d'erreur plus propre
            if shift.bus == self.bus:
                if shift.driver == self.driver:
                    raise ValidationError("This bus and this driver are already booked in a course")
                raise ValidationError("This bus is already booked in a course")
            if shift.driver == self.driver:
                 raise ValidationError("This driver is already booked in a course")

        super(BusShift, self).save(*args, **kwargs)





