from django.db import models


class BusStop(models.Model):
    """
    Model for bus stop, composed with the place of the stop and datetime for
    when it will stop.

    place: fk
    schedule_time: datetime
    """
    place = models.ForeignKey(
        'geography.Place',
        on_delete=models.PROTECT,
        null=False,
        blank=False,
    )
    schedule_time = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=False, blank=False
    )

    def __str__(self):
        return f"Bus Stop: {self.place.name} - {self.schedule_time.strftime('%m/%d/%Y %H:%M')} (id: {self.pk})"


class BusShift(models.Model):
    """
    bus: fk
    driver: fk
    stops: fk m2m (bus shift can have multiple stops, and BusStop can be
    assigned to multiple shift)
    """
    bus = models.ForeignKey(
        'fleet.Bus', on_delete=models.PROTECT, null=False, blank=False,
    )
    driver = models.ForeignKey(
        'fleet.Driver', on_delete=models.PROTECT, null=False, blank=False,
    )
    stops = models.ManyToManyField('BusStop', related_name='bus_shifts')

    @property
    def departure_time(self):
        """
        departure time is the fist value order ASC from list of stops
        :return: datetime
        """
        return self.stops.all().order_by('schedule_time').first().schedule_time

    @property
    def arrival_time(self):
        """
        arrival time is the last value order ASC from list of stops
        :return: datetime
        """
        return self.stops.all().order_by('schedule_time').last().schedule_time

    @property
    def total_time(self):
        """
        duration of a full shift
        :return: timedelta
        """
        return self.arrival_time - self.departure_time

    def __str__(self):
        return f'Bus Shift: Bus:{self.bus.licence_plate}, Driver: {self.driver.user.username} (id: {self.pk})'
