from django import forms
from padam_django.apps.shifts.models import BusShift

class BusShiftForm(forms.ModelForm):
    """ Class to manage the form for the Shift model through Django admin """
    class Meta:
        model = BusShift
        fields = ['bus', 'driver', 'bus_stops']


    def clean(self):
        """ Method to validate the form data based on all criteria """
        cleaned_data = super().clean()
        bus_stops = cleaned_data.get('bus_stops')

        if bus_stops and bus_stops.count() < 2:
            raise forms.ValidationError("A shift must have at least 2 bus stops.")

        if bus_stops:
            start_time = bus_stops.order_by('planned_time').first().planned_time
            end_time = bus_stops.order_by('planned_time').last().planned_time
        else:
            return cleaned_data

        cleaned_data['start_time'] = start_time
        cleaned_data['end_time'] = end_time

        if start_time and end_time:
            overlapping_bus = BusShift.objects.filter(
                bus=self.cleaned_data.get('bus'),
                start_time__lt=cleaned_data['end_time'],
                end_time__gt=cleaned_data['start_time']
            ).exclude(id=self.instance.pk)

            if overlapping_bus.exists():
                raise forms.ValidationError("This shift overlaps with another shift for the same bus.")

            overlapping_driver = BusShift.objects.filter(
                driver=self.cleaned_data.get('driver'),
                start_time__lt=cleaned_data['end_time'],
                end_time__gt=cleaned_data['start_time']
            ).exclude(id=self.instance.pk)

            if overlapping_driver.exists():
                raise forms.ValidationError("This shift overlaps with another shift for the same driver.")

        return cleaned_data

    def save(self, commit=True):
        """ Save the bus shift instance """
        bus_shift = super().save(commit=False)
        bus_shift.start_time = self.cleaned_data['start_time']
        bus_shift.end_time = self.cleaned_data['end_time']

        if commit:
            bus_shift.save()
            bus_shift.bus_stops.set(self.cleaned_data['bus_stops'])

        return bus_shift
