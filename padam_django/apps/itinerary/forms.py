from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .utils import is_driver_possible, is_bus_possible


class BusShiftForm(forms.ModelForm):
    def clean(self):
        bus_stops = self.cleaned_data.get('bus_stops')
        driver = self.cleaned_data.get('driver')
        bus = self.cleaned_data.get('bus')

        if bus_stops.count() < 2:
            raise ValidationError(_('The number of stops is not sufficient to create this busshift.'))

        # TODO : problem for BusShift update : Process only different pk
        if not is_driver_possible(driver, bus_stops):
            raise ValidationError(f"This driver is already busy for this period.")
        if not is_bus_possible(bus, bus_stops):
            raise ValidationError(f"This bus is already in service for this period.")
