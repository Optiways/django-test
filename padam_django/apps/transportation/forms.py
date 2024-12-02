from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from .models import BusShift, BusStop

class BusShiftForm(forms.ModelForm):

    class Meta:
        model = BusShift
        fields = ('bus', 'driver', 'stops')

    def clean(self):
        cleaned_data = super().clean()
        bus = cleaned_data.get('bus')
        stops = cleaned_data.get('stops')
        driver = cleaned_data.get('driver')

        # Check if there are at least two stops
        if stops and stops.count() >= 2:
            departure_time = stops.order_by('arrival_time').first().arrival_time
            arrival_time = stops.order_by('arrival_time').last().arrival_time
        else:
            self.add_error('stops', 'At least two stops are required')
            raise ValidationError('At least two stops are required')

        # Validate the bus and driver availability
        self._validate_bus_availability(bus, departure_time, arrival_time)
        self._validate_driver_availability(driver, departure_time, arrival_time)


    def _validate_bus_availability(self, bus, departure_time, arrival_time):
        existing_shifts = BusShift.objects.filter(bus=bus)
        if self._has_time_conflict(existing_shifts, departure_time, arrival_time):
            raise ValidationError(f'The bus {bus} is already booked during this time period.')

    def _validate_driver_availability(self, driver, departure_time, arrival_time):
        existing_shifts = BusShift.objects.filter(driver=driver)
        if self._has_time_conflict(existing_shifts, departure_time, arrival_time):
            raise ValidationError(f'The driver {driver} is already assigned to another shift during this time period.')

    def _has_time_conflict(self, shifts, start, end):
        for shift in shifts:
            if shift.departure_time <= end and shift.arrival_time >= start:
                return True
        return False