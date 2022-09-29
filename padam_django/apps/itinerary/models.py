from django.db import models


class BusShift(models.Model):
    id = models.BigAutoField(primary_key=True)
    bus = models.ForeignKey("fleet.Bus", on_delete=models.PROTECT)
    driver = models.ForeignKey("fleet.Driver", on_delete=models.PROTECT)
    bus_stops = models.ManyToManyField("itinerary.BusStop", blank=False)
    first_stop = models.DateTimeField(default=None, null=True)
    last_stop = models.DateTimeField(default=None, null=True)

    @property
    def get_start_datetime(self):
        self.first_stop = self.bus_stops.all().order_by('stop_datetime').first()
        if self.first_stop:
            return self.first_stop.stop_datetime
        else:
            return None

    @property
    def get_stop_datetime(self):
        self.last_stop = self.bus_stops.all().order_by('stop_datetime').last()
        if self.last_stop:
            return self.last_stop.stop_datetime
        else:
            return None

    @property
    def get_bus_shift_duration(self):
        return self.bus_stops.all().order_by('stop_datetime').last().stop_datetime \
               - self.bus_stops.all().order_by('stop_datetime').first().stop_datetime

    def __str__(self):
        return f"Bus: {self.bus.licence_plate} driven by {self.driver.user.first_name}" \
               f" {self.driver.user.username}  (id: {self.pk})"


class BusStop(models.Model):
    name = models.CharField("Name of the bus stop", max_length=50)
    place = models.OneToOneField("geography.Place", on_delete=models.CASCADE)
    stop_datetime = models.DateTimeField("Stop time")

    def __str__(self):
        return f"BusStop: {self.name} at {self.place.name}/{self.stop_datetime} (id: {self.pk})"
