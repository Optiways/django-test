from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Model
from django.forms import ModelForm
from django import forms
from datetime import datetime

# Create your models here.
class BusShift(models.Model):
    """
    A bus shift is a period of time during which a bus is driven by a driver and stops at least two bus stops.
    Creating a bus shift is done by creating a BusShiftForm instance.
    """
    bus = models.ForeignKey('fleet.Bus', on_delete=models.CASCADE)
    driver = models.ForeignKey('fleet.Driver', on_delete=models.CASCADE)
    bus_stops = models.ManyToManyField('geography.BusStop')
    start_time = models.TimeField("Start time", blank=True, null=True)
    end_time = models.TimeField("End time", blank=True, null=True)

    @property
    def duration(self):
        start_time = datetime.combine(datetime.today(), self.start_time)
        end_time = datetime.combine(datetime.today(), self.end_time)
        return end_time - start_time

    class Meta:
        unique_together = (("bus", "driver", "start_time"), )

    def __str__(self):
        return (f"BusShift: {self.bus.licence_plate} driven by {self.driver.user.username} at {self.start_time}, duration: {self.duration}, with {self.bus_stops.count()} stops")

class BusShiftForm(ModelForm):
    """
    A form for creating and updating a BusShift instance.
    This has the responsibility of validating the form data and computing the start_time and end_time fields.
    """
    class Meta:
        model = BusShift
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Hide start_time and end_time fields from the form but still compute them in the clean method.
        self.fields['start_time'].widget = forms.HiddenInput()
        self.fields['end_time'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        driver = cleaned_data.get('driver')
        bus = cleaned_data.get('bus')
        bus_stops = cleaned_data.get('bus_stops')

        self.check_bus_stops(bus_stops, cleaned_data)

        self.check_overlapping_shifts(bus, cleaned_data, driver)

        return cleaned_data

    def check_overlapping_shifts(self, bus, cleaned_data, driver):
        """
        Check if the driver or the bus is already scheduled for another shift at this time.
        :param bus:
        :param cleaned_data:
        :param driver:
        :return: 
        """
        overlapping_shifts = BusShift.objects.filter(
            models.Q(driver=driver) | models.Q(bus=bus),
            models.Q(start_time__lt=cleaned_data['end_time'], end_time__gt=cleaned_data['start_time'])
        ).exclude(pk=self.instance.pk)
        if overlapping_shifts.exists():
            raise ValidationError("The driver or the bus is already scheduled for another shift at this time.")

    def check_bus_stops(self, bus_stops, cleaned_data):
        """
        Check if the bus shift has at least two bus stops and sort them by expected arrival time.
        This method alters the cleaned_data dictionary by sorting the bus stops and setting the start_time and end_time fields.
        :param bus_stops:
        :param cleaned_data:
        :return:
        """
        bus_stops_count = bus_stops.count()

        if bus_stops_count < 2:
            raise ValidationError("A bus shift must have at least two bus stops.")
        # Sort and remove duplicates
        cleaned_data['bus_stops'] = sorted(list(set(bus_stops)), key=lambda x: x.expected_arrival)
        last_item = bus_stops_count - 1
        cleaned_data['start_time'] = cleaned_data['bus_stops'][0].expected_arrival
        cleaned_data['end_time'] = cleaned_data['bus_stops'][last_item].expected_arrival

