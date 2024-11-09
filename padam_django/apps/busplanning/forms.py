from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from padam_django.apps.busplanning.models import BusShift
from padam_django.apps.fleet.models import Driver


class BusShiftForm(forms.ModelForm):
    class Meta:
        model = BusShift
        fields = "__all__"
        # TODO add ModelChoiceField to add the BusStops at the creation

    def clean(self):
        cleaned_data = super().clean()
        driver = cleaned_data["driver"]
        bus = cleaned_data["bus"]
        departure = cleaned_data["start_time"]
        arrival = cleaned_data["end_time"]

        # Get overlapping schedules for driver or buses:
        # For any driver or matching bus:
        # - start_time < departure < end_time: if the departure overlaps
        # - start_time < arrival < end_time: if the arrival overlaps
        # - departure < star_time < arrival: if another shift begins during this one
        # Any result os overlapping
        overlapping_shifts = BusShift.objects.filter(
            Q(
                Q(driver=driver) | Q(bus=bus)
            ) &
            Q(
                Q(start_time__lte=departure, end_time__gte=departure) |
                Q(start_time__lte=arrival, end_time__gte=arrival) |
                Q(start_time__gte=departure, end_time__lte=arrival)
            )
        )
        print(overlapping_shifts)
        if len(overlapping_shifts) > 0:
            raise ValidationError(
                "Schedule is overlapping with other schedules: %(schedules)s",
                code="overlapping",
                params={"schedules": overlapping_shifts}
            )

        return self.cleaned_data
