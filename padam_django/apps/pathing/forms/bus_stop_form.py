from django import forms
from padam_django.apps.geography.models import Place
from padam_django.apps.pathing.models.bus_stop import BusStop
from django.core.exceptions import ValidationError

class BusStopForm(forms.ModelForm):
    class Meta:
        model = BusStop
        fields = ['visit_date_time', 'place']


