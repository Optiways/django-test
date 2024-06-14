from django import forms
from django.core.exceptions import ValidationError

from .models import BusShift, ScheduleStop


class ScheduleStopForm(forms.ModelForm):
    class Meta:
        model = ScheduleStop
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        bus_shift = cleaned_data["bus_shift"]
        arrival = cleaned_data["arrival"]

        # Check bus
        bus_shifts = BusShift.objects.filter(
            bus=bus_shift.bus, first_stop__lte=arrival, last_stop__gte=arrival
        ).count()

        if bus_shifts > 0:
            raise ValidationError("Bus is not available")

        driver_shifts = BusShift.objects.filter(
            driver=bus_shift.driver, first_stop__lte=arrival, last_stop__gte=arrival
        ).count()

        if driver_shifts > 0:
            raise ValidationError("Driver is not available")

        return cleaned_data
