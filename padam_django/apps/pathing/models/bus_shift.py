from django.db import models
from padam_django.apps.fleet.models import Bus, Driver


class BusShift(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name="bus_shifts")
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="bus_shifts")

    class Meta:
        verbose_name = "Bus Shift"
        verbose_name_plural = "Bus Shifts"

    def get_ordered_bus_stops(self):
        return sorted(self.bus_stops.all(), key=lambda stop: stop.visit_date_time)

    def get_departure(self):
        return self.get_ordered_bus_stops()[0]

    def get_arrival(self):
        return self.get_ordered_bus_stops()[-1]

    def get_travel_time(self):
        return self.get_arrival().visit_date_time - self.get_departure().visit_date_time

    def __str__(self):
        return f"{self.id} - {self.bus} - {self.driver}"