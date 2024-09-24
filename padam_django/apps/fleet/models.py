from django.db import models


class Driver(models.Model):
    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="driver"
    )

    def __str__(self):
        return f"Driver: {self.user.username} (id: {self.pk})"


class Bus(models.Model):
    licence_plate = models.CharField("Name of the bus", max_length=10)

    class Meta:
        verbose_name_plural = "Buses"

    def __str__(self):
        return f"Bus: {self.licence_plate} (id: {self.pk})"


class BusStop(models.Model):
    name = models.CharField("Name of the bus stop", max_length=200)
    place = models.OneToOneField(
        "geography.Place", on_delete=models.PROTECT, related_name="bus_stop"
    )

    class Meta:
        verbose_name = "Bus stop"
        verbose_name_plural = "Bus stops"

    def __str__(self):
        return f"Bus stop: {self.name} (id: {self.pk})"


class BusShiftScheduledStop(models.Model):
    stop = models.ForeignKey("fleet.BusStop", on_delete=models.CASCADE)
    shift = models.ForeignKey(
        "fleet.BusShift",
        on_delete=models.CASCADE,
        related_name="scheduled_stops",
        related_query_name="scheduled_stop",
    )
    time = models.TimeField("Time of passage through the stop")

    class Meta:
        ordering = ("time",)
        constraints = (
            models.UniqueConstraint(
                name="unique_for_stop_shift", fields=("stop", "shift")
            ),
            models.UniqueConstraint(
                name="unique_for_shift_time", fields=("shift", "time")
            ),
        )

    def __str__(self):
        return f"{self.stop.name} {self.time}"


class BusShiftQueryset(models.QuerySet):
    def overlapping(self, departure, arrival):
        return self.filter(
            scheduled_stop__time__gte=departure,
            scheduled_stop__time__lte=arrival,
        )


class BusShift(models.Model):
    objects = BusShiftQueryset.as_manager()
    bus = models.ForeignKey(
        "fleet.Bus",
        on_delete=models.PROTECT,
        related_name="shifts",
        related_query_name="shift",
    )
    driver = models.ForeignKey(
        "fleet.Driver",
        on_delete=models.PROTECT,
        related_name="shifts",
        related_query_name="shift",
    )
    stops = models.ManyToManyField(
        "fleet.BusStop",
        through=BusShiftScheduledStop,
        related_name="shifts",
        related_query_name="shift",
    )

    def departure(self):
        return self.scheduled_stops.order_by("time").first()

    def arrival(self):
        return self.scheduled_stops.order_by("time").last()

    def time_range(self):
        return self.departure().time, self.arrival().time

    class Meta:
        verbose_name = "Bus shift"
        verbose_name_plural = "Bus shifts"

    def __str__(self):
        return f"Bus shift: {self.departure()} — {self.arrival()} (id: {self.pk})"
