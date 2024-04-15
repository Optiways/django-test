from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet

from ..fleet.models import Bus, Driver
from .models import BusShift


class BusShiftForm(forms.ModelForm):

    class Meta:
        """Meta class to define the model and fields used in the form."""
        model = BusShift
        fields = ('bus', 'driver', 'stops') 

    def clean(self) -> None:
        """
        Clean method to validate the form data.

        Validates the following fields:
        - bus: Check if the bus is available during the selected time frame.
        - driver: Check if the driver is available during the selected time frame.
        - stops: Check if there are at least two bus stops.

        Raises a ValidationError if any of the validations fail.
        """
        cleaned_data = super().clean()
        bus = cleaned_data.get('bus')
        stops = cleaned_data.get('stops')
        driver = cleaned_data.get('driver')
        if stops:
            departure_time = stops.order_by('transit_time').first().transit_time
            arrival_time = stops.order_by('transit_time').last().transit_time
        
        self._check_two_stops_at_least(stops)
        self._check_bus_availability(departure_time, arrival_time, bus)
        self._check_driver_availability(departure_time, arrival_time, driver)

    def _check_bus_availability(self, departure_time: datetime, arrival_time: datetime, bus: Bus) -> None:
        """
        Check if the given bus is available during the given time range.

        Args:
            departure_time (datetime): The departure time of the bus shift.
            arrival_time (datetime): The arrival time of the bus shift.
            bus (Bus): The bus object to check availability for.

        Raises:
            ValidationError: If the given bus is already in use during the given time range.
        """
        shifts = BusShift.objects.filter(bus__pk=bus.pk)
        if not self._is_available(shifts, departure_time, arrival_time):
            raise ValidationError('This bus is already booked for a shift')

    def _check_driver_availability(self, departure_time: datetime, arrival_time: datetime, driver: Driver) -> None:
        """
        Check if the selected driver is available during the specified shift time.

        Args:
            departure_time (datetime): The departure time of the bus shift.
            arrival_time (datetime): The arrival time of the bus shift.
            driver (Driver): The Driver object representing the selected driver for the bus shift.

        Raises:
            ValidationError: If the driver is already assigned to another shift during the specified time period.
        """
        shifts = BusShift.objects.filter(driver__pk=driver.pk)
        if not self._is_available(shifts, departure_time, arrival_time):
            raise ValidationError('This driver is already on a shift')

    @staticmethod
    def _is_available(shifts: QuerySet, departure_time: datetime, arrival_time: datetime) -> bool:  
        """
        Check if there is no overlap between the given shifts and the time range defined by the
        departure and arrival times.

        Args:
            shifts (QuerySet): A queryset of BusShift instances to compare against.
            departure_time (datetime): The departure time of the new shift to be created.
            arrival_time (datetime): The arrival time of the new shift to be created.

        Returns:
            bool: True if there is no overlap between the shifts and the given time range, False otherwise.
        """
        return not any(
            (shift.departure_time <= departure_time <= shift.arrival_time) or
            (shift.departure_time <= arrival_time <= shift.arrival_time) or
            (shift.departure_time >= departure_time and shift.arrival_time <= arrival_time)
            for shift in shifts
        )

    @staticmethod
    def _check_two_stops_at_least(stops: QuerySet) -> None:
        """Validate that at least two bus stops are provided.

        Args:
            stops (QuerySet): The set of bus stops included in the shift.

        Raises:
            ValidationError: Raised if less than two bus stops are included in the shift.
        """
        if stops.count() < 2:
            raise ValidationError('At least two stops are required')
