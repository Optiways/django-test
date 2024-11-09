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
        start_time = cleaned_data["start_time"]
        end_time = cleaned_data["end_time"]

        # get overlapping schedules for driver or buses
        overlapping_shifts = BusShift.objects.filter(
            Q(
                Q(driver=driver) | Q(bus=bus)
            ) &
            Q(
                Q(start_time__lte=start_time, end_time__gte=start_time) |
                Q(start_time__lte=end_time, end_time__gte=end_time) |
                Q(start_time__gte=start_time, end_time__lte=end_time)
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
