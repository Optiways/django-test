from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, ValidationError

from .models import BusShift, BusStop


class BusStopForm(forms.ModelForm):
    class Meta:
        model = BusStop
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        arrival_time = cleaned_data.get("arrival_time")
        departure_time = cleaned_data.get("departure_time")

        if arrival_time is None and departure_time is None:
            raise ValidationError(
                "Either Arrival time or Departure time must be provided."
            )

        if arrival_time and departure_time and arrival_time <= departure_time:
            raise ValidationError("Arrival time must be before departure time.")

        return cleaned_data


class BusShiftAdminForm(ModelForm):
    class Meta:
        model = BusShift
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        bus = cleaned_data.get("bus")
        driver = cleaned_data.get("driver")
        stops = cleaned_data.get("stops")

        self._validate_minimum_stops(stops)
        start_time, end_time = self._get_shift_times(stops)
        self._validate_shift_times(start_time, end_time)
        self._validate_no_overlapping_shifts(bus, driver, start_time, end_time)

        return cleaned_data

    def _validate_minimum_stops(self, stops):
        if not stops or len(stops) < 2:
            raise ValidationError("A BusShift must have at least 2 stops.")

    def _get_shift_times(self, stops):
        start_time = (
            stops.exclude(departure_time__isnull=True)
            .order_by("departure_time")
            .first()
            .departure_time
        )
        end_time = (
            stops.exclude(arrival_time__isnull=True)
            .order_by("arrival_time")
            .last()
            .arrival_time
        )
        return start_time, end_time

    def _validate_shift_times(self, start_time, end_time):
        if not start_time or not end_time:
            raise ValidationError(
                "Both start time and end time must be defined for the shift."
            )

    def _validate_no_overlapping_shifts(self, bus, driver, start_time, end_time):
        self._check_overlapping_shifts(bus, start_time, end_time, "bus")
        self._check_overlapping_shifts(driver, start_time, end_time, "driver")

    def _check_overlapping_shifts(self, entity, start_time, end_time, entity_type):
        overlapping_shifts = BusShift.objects.exclude(pk=self.instance.pk).filter(
            **{entity_type: entity}
        )
        for shift in overlapping_shifts:
            shift_start_time = shift.start_time
            shift_end_time = shift.end_time
            if shift_start_time and shift_end_time:
                if shift_start_time < end_time and shift_end_time > start_time:
                    raise ValidationError(
                        f"This {entity_type} is already assigned to another overlapping shift."
                    )
