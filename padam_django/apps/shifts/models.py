from django.db import models



class BusStop(models.Model):
    """ Model representing a bus stop. """
    place = models.ForeignKey('geography.Place', on_delete=models.CASCADE, related_name='bus_stops')
    planned_time = models.DateTimeField(auto_now=False, auto_now_add=False)

    class Meta:
        ordering = ['planned_time']
        # Two Bus stops can't have the same planned time and place
        unique_together = ['place', 'planned_time']

    def __str__(self):
        """ String for representing the BusStop instance. """
        planned_time = self.planned_time.strftime("%B %d, %Y, %I:%M %p")
        return f"{self.place.name.upper()} at {planned_time}"


class BusShift(models.Model):
    """ Model representing a bus shift. """
    bus = models.ForeignKey('fleet.Bus', on_delete=models.CASCADE,null=False, blank=False, related_name='shifts')
    driver = models.ForeignKey('fleet.Driver', on_delete=models.CASCADE, null=False,blank=False,related_name='bus_shifts')
    bus_stops = models.ManyToManyField(BusStop, blank=False, related_name='bus_shifts')
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    def __str__(self):
        """ String representation of the BusShift instance. """
        return f"Bus Shift: {self.bus} with driver {self.driver} from {self.start_time} to {self.end_time}"

    def calculate_start_time(self):
        """Returns the start time of the shift, which is the time of the first bus stop."""
        if not self.pk:
            return

        ordered_stops = self.bus_stops.order_by('planned_time')
        if ordered_stops.exists():
            self.start_time = ordered_stops.first().planned_time

    def calculate_end_time(self):
        """" Returns the end time of the shift which is the time of the last bus stop. """
        if not self.pk:
            return
        ordered_stops = self.bus_stops.order_by('planned_time')
        if ordered_stops.exists():
            self.end_time = ordered_stops.last().planned_time


    @property
    def total_duration_seconds(self):
        """Calculates the total duration (in seconds) based on start and end times of the shift."""
        if self.start_time and self.end_time:
            time_difference = self.end_time - self.start_time
            return time_difference.total_seconds()
        return

    def save(self, *args, **kwargs):
        """ Save the BusShift instance """
        super().save(*args, **kwargs)
        if self.bus_stops.exists():
            self.calculate_start_time()
            self.calculate_end_time()
            super().save(update_fields=['start_time', 'end_time'])  # Sauvegarder uniquement les champs modifiés



