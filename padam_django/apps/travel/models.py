from django.db import models
from datetime import timedelta

class BusStop(models.Model):

    name = models.CharField("Name of the bus stop", max_length=50)
    place = models.ForeignKey("geography.Place", on_delete=models.CASCADE)

    def __str__(self):
        return f"BusStop: {self.name} at {self.place.name} (id: {self.pk})"

class BusShift(models.Model):

    bus = models.ForeignKey("fleet.Bus", on_delete=models.PROTECT)
    driver = models.ForeignKey("fleet.Driver", on_delete=models.PROTECT)
    departure_stop = models.ForeignKey("BusStopDate",
                                       on_delete=models.PROTECT,
                                       related_name="departure_stop")
    arrival_stop = models.ForeignKey("BusStopDate", on_delete=models.PROTECT,
                                     related_name="arrival_stop")
    intermediate_stops = models.ManyToManyField("BusStopDate", null=True,
                                                blank=True,
                                                related_name="intermediate_stop")

    @property
    def departure_time(self):
        return self.departure_stop.time

    @property
    def arrival_time(self):
        return self.arrival_stop.time

    @property
    def travel_time(self):
        return timedelta(hours=self.arrival_time.hour,
                  minutes=self.arrival_time.minute, seconds =
                  self.arrival_time.second) \
               -\
               timedelta(hours=self.departure_time.hour,
                  minutes=self.departure_time.minute, seconds =
                  self.departure_time.second)

    def __str__(self):
        return f"BusShift of {self.driver.user} from " \
               f"{self.departure_stop.bus_stop.name} to" \
               f" {self.arrival_stop.bus_stop.name}"

day_choices = (
        ("monday", "Monday"),
        ("tuesday", "Tuesday"),
        ("wednesday", "Wednesday"),
        ("thursday", "Thursday"),
        ("friday", "Friday"),
        ("saturday", "Saturday"),
        ("sunday", "Sunday"),
)
class BusStopDate(models.Model):

    bus_stop = models.ForeignKey("BusStop", on_delete=models.CASCADE)

    # Can be improved with m2m field and a constant "day" table, not visible
    # in admin, populated in migration. I'm doing this because I'm short in time
    day = models.CharField(choices=day_choices, max_length=10, null=True)
    time = models.TimeField(null=True)

    def __str__(self):
        return f"BusStopDate: {self.bus_stop.name} on {self.day}" \
               f" {self.time} (id:" \
               f" {self.pk})"
