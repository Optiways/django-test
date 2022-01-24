from pickle import TRUE
from django.db import models
from padam_django.apps.geography.models import Place
from padam_django.apps.fleet.models import Driver, Bus
from padam_django.apps.busservice.exceptions import BusOrDriverOccupiedError
from django.db.models import Count


class BusShift(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.RESTRICT, null=True, blank=True)
    bus = models.ForeignKey(Bus, on_delete=models.RESTRICT, null=True, blank=True)

    @property
    def start_time(self):
        bus_stops = self.busstops
        if bus_stops.exists():
            return self.busstops.order_by("timestamp").first().timestamp
        return None

    @property
    def end_time(self):
        bus_stops = self.busstops
        if bus_stops.exists():
            return self.busstops.order_by("timestamp").last().timestamp
        return None

    def is_during_shift(self, timestamp):
        if self.busstops.count() < 2:
            return False
        return self.start_time <= timestamp <= self.end_time

    def __str__(self):
        return f"{self.bus} , {self.driver}, (id: {self.pk})"


class BusStop(models.Model):
    place = models.ForeignKey(Place, on_delete=models.RESTRICT)
    timestamp = models.DateTimeField()
    busshift = models.ForeignKey(
        BusShift, on_delete=models.RESTRICT, related_name="busstops"
    )

    def is_overlapping(self):
        """check if created BusStop is overlapping with existing one"""
        # TODO : merge queryset
        driver_shifts = (
            BusShift.objects.filter(driver=self.busshift.driver)
            .annotate(busstop_count=Count("busstops"))
            .exclude(id=self.busshift.id)
            .exclude(busstop_count__lt=2)
        )

        if driver_shifts.exists():
            for driver_shift in driver_shifts:
                if driver_shift.is_during_shift(self.timestamp):
                    return True

        bus_shifts = (
            BusShift.objects.filter(bus=self.busshift.bus)
            .annotate(busstop_count=Count("busstops"))
            .exclude(id=self.busshift.id)
            .exclude(busstop_count__lt=2)
        )

        if bus_shifts.exists():
            for bus_shift in bus_shifts:
                if bus_shift.is_during_shift(self.timestamp):
                    return True

        return False

    def save(self, *args, **kwargs) -> None:
        if self.is_overlapping():
            raise BusOrDriverOccupiedError
        return super(BusStop, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.place}, {self.timestamp}"
