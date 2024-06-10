from django import forms
from django.core.exceptions import ValidationError

from .models import BusShift


class BusShiftForm(forms.ModelForm):
    class Meta:
        model = BusShift
        fields = ['bus', 'driver', 'stop']

    def clean(self):
        """
        Check if bus or driver is available
        :return: Raise an error if the bus or driver is not available
        """

        bus = self.cleaned_data.get('bus')
        driver = self.cleaned_data.get('driver')
        stop = self.cleaned_data.get('stop')

        if stop is not None:
            bus_available = bus.available_at(stop.first().stop_datetime)
            if not bus_available:
                raise ValidationError(f"{bus} is not available at that time")

            driver_available = driver.available_at(stop.last().stop_datetime)
            if not driver_available:
                raise ValidationError(f"{driver} is not available at that time")
