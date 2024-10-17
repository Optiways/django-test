from datetime import datetime

from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import BusShift, BusStop

from django.forms import BaseInlineFormSet


class BusShiftFormSet(BaseInlineFormSet):

    def clean(self):
        super().clean()

        if any([bool(value) for value in self.errors]):
            return None

        bus_stops = [bus_stop for bus_stop in self.cleaned_data if not bus_stop.get('DELETE', False)]
        bus_stops_deleted = [bus_stop for bus_stop in self.cleaned_data if bus_stop.get('DELETE', False)]
        bus_shift: BusShift = self.instance

        can_be_deleted = all([bool(bus_stop_deleted["id"].transit_time > timezone.now()) for bus_stop_deleted in bus_stops_deleted])

        if not can_be_deleted:
            raise ValidationError("Cannot delete a Bus stop that is in the past.")

        if len(bus_stops) < 2:
            raise ValidationError('At least two bus stops are required.')

        bus_stops.sort(key=lambda x: x['transit_time'])

        start_transit_time = bus_stops[0]['transit_time']
        end_transit_time = bus_stops[-1]['transit_time']

        # Check if the driver and the bus are available during the transit time period
        if not bus_shift.driver.is_available(start_transit_time, end_transit_time, bus_shift.pk):
            raise ValidationError('Bus driver is not available during all the period of the shift.')

        if not bus_shift.bus.is_available(start_transit_time, end_transit_time, bus_shift.pk):
            raise ValidationError('Bus is not available during all the period of the shift.')

class BusStopForm(forms.ModelForm):
    class Meta:
        model = BusShift
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        bus_stop: BusStop = cleaned_data.get('id')
        bus_shift: BusShift = cleaned_data.get("bus_shift")
        transit_time: datetime = cleaned_data.get("transit_time")
        to_delete = cleaned_data.get("DELETE")

        # TODO: make it a bit more clean ...
        # If the instance is not defined just check if the transit time is not in the past
        if bus_shift.pk is None:
            if timezone.now() > transit_time:
                return self.add_error(None, ValidationError("You can't set a stop in the past"))
            return cleaned_data

        if bus_stop is None and not bus_shift.can_add_stop(transit_time):
            return self.add_error(None, ValidationError(
                "The Current Bus shift is already ended or the transit time is in the past."))

        if bus_stop is not None and bus_stop.transit_time != transit_time and not bus_stop.can_modify_stop(transit_time):
            return self.add_error(None, ValidationError(
                "The Current Bus shift is already ended or the transit time is in the past."))

        return cleaned_data


class BusShiftForm(forms.ModelForm):
    class Meta:
        model = BusShift
        fields = '__all__'
