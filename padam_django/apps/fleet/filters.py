
# Django import.
from django import forms

# App import.
from . import models


def bus_stop_filter_by(user, date):
    class StopsForm(forms.ModelForm):
        bus_stop = forms.ModelChoiceField(
            queryset=models.BusStop.objects.filter(
                driver__user=user,
                date=date
            )
        ) 
    return StopsForm


def driver_filter_by(user):
    class DriverForm(forms.ModelForm):
        driver = forms.ModelChoiceField(
            queryset=models.Driver.objects.filter(
                user=user,
            ),
        ) 
    return DriverForm
