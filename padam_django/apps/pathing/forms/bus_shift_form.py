from django import forms
from padam_django.apps.pathing.models.bus_shift import BusShift
from padam_django.apps.pathing.models.bus_stop import BusStop
from django.core.exceptions import ValidationError

class BusShiftForm(forms.ModelForm):
    bus_stops = forms.ModelMultipleChoiceField(
        queryset=BusStop.objects.filter(bus_shift__isnull=True),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select Bus Stops"
    )

    class Meta:
        model = BusShift
        fields = ['bus', 'driver']

    def clean_bus_stops(self):
        bus_stops = self.cleaned_data.get('bus_stops')
        if len(bus_stops) < 2:
            raise ValidationError("You must select at least 2 bus stops.")

        bus = self.cleaned_data.get('bus')
        driver = self.cleaned_data.get('driver')
        bus_stops = self.cleaned_data.get('bus_stops')

        ordered_stops = sorted(bus_stops, key=lambda stop: stop.visit_date_time)
        departure_time = ordered_stops[0].visit_date_time
        arrival_time = ordered_stops[-1].visit_date_time

        overlapping_bus_shifts = BusShift.objects.filter(
            bus=bus,
            bus_stops__visit_date_time__lt=arrival_time,
            bus_stops__visit_date_time__gt=departure_time,
        ).exclude(pk=self.instance.pk)

        overlapping_driver_shifts = BusShift.objects.filter(
            driver=driver,
            bus_stops__visit_date_time__lt=arrival_time,
            bus_stops__visit_date_time__gt=departure_time,
        )

        if overlapping_bus_shifts.exists() or overlapping_driver_shifts.exists():
            raise ValidationError("This bus or driver is already assigned to a shift during this time.")

        return bus_stops