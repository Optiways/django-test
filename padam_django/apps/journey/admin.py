from django.contrib import admin
from django.forms import *

from . import models
from .models import BusShift
from ..geography.admin import BusStopInline


class BusShiftAdminForm(ModelForm):

    class Meta:
        model = BusShift
        fields = ['bus', 'driver']


@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    list_display = ('bus', 'driver', 'departure_time', 'arrival_time', 'journey_duration')
    form = BusShiftAdminForm

    inlines = [
        BusStopInline
    ]
