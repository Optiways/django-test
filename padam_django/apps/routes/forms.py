from django import forms
from django.core.exceptions import ValidationError

from . import models


class BusShiftForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        bus = cleaned_data.get('bus')
        stops_qs = cleaned_data.get('stops')
        driver = cleaned_data.get('driver')
        # getting departure time from 1st bus stop
        departure_time = stops_qs.order_by('schedule_time').first().schedule_time
        # getting arrival time from last bus stop
        arrival_time = stops_qs.order_by('schedule_time').last().schedule_time
        # check business constraints validation
        self._check_two_stops_at_least(stops_qs)
        self._check_bus_available(departure_time, arrival_time, bus)
        self._check_driver_available(departure_time, arrival_time, driver)

    def _check_bus_available(self, departure_time, arrival_time, bus):
        """
        :param departure_time: datetime
        :param arrival_time: datetime
        :param bus: Bus instance

        Raise validation if bus is not available during shift time planned
        """
        shifts = models.BusShift.objects.filter(bus__pk=bus.pk)
        shifts = self.exclude_own_shift(shifts)
        if not self.is_available(shifts, departure_time, arrival_time):
            raise ValidationError('Bus already use in a shift')

    def _check_driver_available(self, departure_time, arrival_time, driver):
        """
        :param departure_time: datetime
        :param arrival_time: datetime
        :param driver: Driver instance

        Raise validation if driver is not available during shift time planned
        """
        shifts = models.BusShift.objects.filter(driver__pk=driver.pk)
        shifts = self.exclude_own_shift(shifts)
        if not self.is_available(shifts, departure_time, arrival_time):
            raise ValidationError('Driver already use in a shift')

    def exclude_own_shift(self, shifts):
        """
        :param shifts: BusShift QuerySet
        :return: BusShift QuerySet

        If form is updating shift, we need to exclude the actual shift of list
        of BusShifts QuerySet in order to take in account that Driver or Bus is
        used by it own initial shift value.
        """
        is_insert = self.instance.pk is None
        updated_shifts = shifts
        if not is_insert:
            updated_shifts = shifts.exclude(pk=self.instance.pk)
        return updated_shifts

    @staticmethod
    def is_available(shifts, departure_time, arrival_time):
        """
        :param shifts: BusShift Queryset
        :param departure_time: datetime
        :param arrival_time: datetime
        :return: bool

        check if departure and arrival time slots chosen are not used on other
        shifts
        """
        for shift in shifts:
            # check if departure is not between another departure and arrival
            if shift.departure_time <= departure_time <= shift.arrival_time:
                return False
            # check if arrival is not between another departure and arrival
            if shift.departure_time <= arrival_time <= shift.arrival_time:
                return False
            # check that departure before another shift departure and
            # arrival after another shift arrival is not possible
            if shift.departure_time >= departure_time and shift.arrival_time <= arrival_time:
                return False
        return True

    @staticmethod
    def _check_two_stops_at_least(stops_qs):
        """
        :param stops_qs: BusStop QuerySet

        Shift must have at least 2 stops. If not raised validation error
        """
        if stops_qs.count() < 2:
            raise ValidationError('Two bus stops needed at least')
