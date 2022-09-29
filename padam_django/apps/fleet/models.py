from django.db import models
from django.core.exceptions import ValidationError

from padam_django.apps.geography.models import BusStop


class Driver(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='driver')

    def __str__(self):
        return f"Driver: {self.user.username} (id: {self.pk})"


class Bus(models.Model):
    licence_plate = models.CharField("Name of the bus", max_length=10)

    class Meta:
        verbose_name_plural = "Buses"

    def __str__(self):
        return f"Bus: {self.licence_plate} (id: {self.pk})"


class BusShift(models.Model):
    """Define a Bus Shift Model Data
    :model:
        `Bus`
        `Driver`
        `geography.BusStop`
    """

    bus = models.ForeignKey(
        Bus, on_delete=models.RESTRICT, related_name="buses", null=True
    )
    driver = models.ForeignKey(
        Driver, on_delete=models.RESTRICT, related_name="drivers", null=True
    )

    # I'm defining a starting bus stop as I consider it an important information for the shift
    starting_stop = models.ForeignKey(
        BusStop, on_delete=models.RESTRICT, related_name="starting_stop"
    )
    stops = models.ManyToManyField(BusStop)

    # Assuming that long distance shift can exist, I define time as DateTimeField and not only TimeField
    start_time = models.DateTimeField(help_text="Shift start time")
    end_time = models.DateTimeField(help_text="Shift end time")

    @property
    def shift_duration(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None

    def __str__(self):
        return f"""Bus Shift : ({self.pk}) (Driver: {self.driver}) (Bus: {self.bus})
                (Start: {self.start_time}) (End: {self.end_time}) - (Duration: {self.shift_duration})"""

    def check_available_bus(self):
        """Check available bus on the shift according to start and end time.
        If selected bus is used on another crossing time bus shift, raise a validation error
        Raises:
            ValidationError
        """
        buses_shifts = BusShift.objects.filter(bus=self.bus).filter(
            start_time__lte=self.end_time, end_time__gte=self.start_time
        )
        if buses_shifts:
            raise ValidationError(
                f"Cannot set bus {self.bus}, used in another time crossing shift"
            )

    def check_available_driver(self):
        """Check available driver on the shift according to start and end time.
        If selected driver is planned on another crossing time bus shift, raise a validation error
        Raises:
            ValidationError
        """
        drivers_shifts = BusShift.objects.filter(driver=self.driver).filter(
            start_time__lte=self.end_time, end_time__gte=self.start_time
        )
        if drivers_shifts:
            raise ValidationError(
                f"Cannot set driver {self.driver}, used in another time crossing shift"
            )

    def clean(self):
        self.is_cleaned = True

        self.check_available_bus()
        self.check_available_driver()

        super(BusShift, self).clean()

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.full_clean()
        super(BusShift, self).save(*args, **kwargs)