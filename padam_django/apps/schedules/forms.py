from django import forms
from padam_django.apps.schedules.models import BusShift, BusStop


class BusShiftForm(forms.ModelForm):
    class Meta:
        model = BusShift
        fields = ["driver", "bus"]
