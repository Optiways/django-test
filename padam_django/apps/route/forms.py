from typing import Dict

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import BusShift

class BusShiftForm(forms.ModelForm):
    class Meta:
        model = BusShift
        fields = ['bus', 'driver', 'stops']

    def clean(self) -> Dict:
        """
            Checking whether a bus or a driver is already busy
        """

        bus = self.cleaned_data.get('bus')
        driver = self.cleaned_data.get('driver')
        stops = self.cleaned_data.get('stops')

        is_bus_available = bus.is_available_at(stops.first().date)
        if not is_bus_available:
            raise ValidationError(_(f"{bus} is not available at that time"))

        is_driver_available = driver.is_available_at(stops.last().date)
        if not is_driver_available:
            raise ValidationError(_(f"{driver} is not available at that time"))
