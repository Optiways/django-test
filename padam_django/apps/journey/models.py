from django.db import models


class BusShift(models.Model):
    bus = models.ForeignKey('fleet.Bus', on_delete=models.PROTECT, related_name='bus_shift')
    driver = models.ForeignKey('fleet.Driver', on_delete=models.PROTECT, related_name='bus_shift')

    @property
    def bus_stops(self):
        """Ordered list of bus stop order by pickup time.
        :rtype: QuerySet[BusStop]
        """
        return self.bus_stop.order_by('pickup_time')

    @property
    def departure_time(self):
        """Departure time determined as the first bus stop pickup time.
        :rtype: DateTime
        """
        if self.bus_stops:
            first_stop = self.bus_stops.earliest('pickup_time')
            return first_stop.pickup_time
        return None

    @property
    def arrival_time(self):
        """Departure time determined as the last bus stop pickup time.
        :rtype: DateTime
        """
        if self.bus_stops:
            last_stop = self.bus_stops.latest('pickup_time')
            return last_stop.pickup_time
        return None

    @property
    def journey_duration(self):
        """Return journey duration in seconds.
        :rtype: str
        """
        time_delta = self.arrival_time - self.departure_time
        return time_delta.total_seconds()

    def __str__(self):
        return f"BusShift: Planned from {self.departure_time} to {self.arrival_time} " \
               f"with bus {self.bus.licence_plate} (id: {self.pk})"
