from django.db import models
from django.db.models import Max, Min, Q


class BusShift(models.Model):
    driver = models.ForeignKey("fleet.Driver", on_delete=models.CASCADE)
    bus = models.ForeignKey("fleet.Bus", on_delete=models.CASCADE)
    stops = models.ManyToManyField("geography.Place", through="schedules.BusStop")

    def __str__(self):
        return f"Bus Shift: {self.driver} {self.bus}"

    def shift_is_available(self, start_time, end_time):
        """Returns False if there's already a shift for the bus or driver that
        overlaps a given start_time and end_time

        :param start_time: start time of the range to check
        :type start_time: datetime.time
        :param end_time: end time of the range to check
        :type end_time: datetime.time
        :return: True or False
        :rtype: bool
        """
        return (
            not BusStop.objects.filter(
                Q(shift__bus=self.bus) | Q(shift__driver=self.driver)
            )
            .values("shift__id")
            .annotate(start=Min("stoptime"), end=Max("stoptime"))
            .filter(
                Q(start__range=(start_time, end_time))
                | Q(end__range=(start_time, end_time))
                | Q(start__lte=start_time, end__gte=end_time)
            )
            .exists()
        )


class BusStop(models.Model):
    shift = models.ForeignKey("schedules.BusShift", on_delete=models.CASCADE)
    place = models.ForeignKey("geography.Place", on_delete=models.CASCADE)
    stoptime = models.TimeField("Stop time")

    def __str__(self):
        return f"Bus Stop: {self.shift_id} {self.stoptime}"
