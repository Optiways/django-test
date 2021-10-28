from django.db import models


class BusShift(models.Model):
    bus = models.ForeignKey("fleet.Bus", on_delete=models.CASCADE)
    driver = models.ForeignKey("fleet.Driver", on_delete=models.CASCADE)
    bus_stops = models.ManyToManyField("BusStop")

    departure_time = models.DateTimeField(blank=True, null=True)
    arrival_time = models.DateTimeField(blank=True, null=True)

    @property
    def duration(self):
        if self.arrival_time is not None and self.departure_time is not None:
            return self.arrival_time - self.departure_time

    def is_available(self):
        pass

    # Constraint Check if instance of shift has bus/driver and is not in timetable of departure/arrival of another
    #   instance, UniqueConstraint doesnt stop from creating instances without the necessary constraints
    # If I had the time for this , I could search on a query for driver/bus and check every row depending on time
    #   I would also need to add validation , though I would usually do this on a view
    # https://docs.djangoproject.com/en/3.2/ref/models/constraints/#django.db.models.UniqueConstraint
    # https://docs.djangoproject.com/en/3.2/topics/db/queries/#complex-lookups-with-q

    # This currently does not work , I'll leave it in for now
    class Meta:
        # constraint = [
        #     models.CheckConstraint(check=models.Q())
        # ]
        models.UniqueConstraint(fields=['bus', 'departure_time', 'arrival_time'], name='unique_bus_booking')
        models.UniqueConstraint(fields=['driver', 'departure_time', 'arrival_time'], name='unique_driver_booking')

    def __str__(self):
        return f"Time Table: {self.departure_time} - {self.arrival_time} (id: {self.pk})"


class BusStop(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True)
    place = models.ForeignKey("geography.Place", on_delete=models.CASCADE)
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['time']

    def __str__(self):
        if self.name:
            return f"Place: {self.name} at {self.place.name} (id: {self.pk})"
        else:
            return f"Place: {self.place.name} (id: {self.pk})"
