from django.db import models

class BusShift(models.Model):
    driver = models.ForeignKey("fleet.Driver", on_delete=models.CASCADE)
    bus = models.ForeignKey("fleet.Bus", on_delete=models.CASCADE)
    stops = models.ManyToManyField("geography.Place", through="schedules.BusStop")

    def __str__(self):
        return f"Bus Shift: {self.driver} {self.bus}"


class BusStop(models.Model):
    shift = models.ForeignKey("schedules.BusShift", on_delete=models.CASCADE)
    place = models.ForeignKey("geography.Place", on_delete=models.CASCADE)
    stoptime = models.TimeField("Stop time")