from django.contrib import admin

from . import models
from . import forms


@admin.register(models.BusStop)
class BusStopAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'place', 'schedule_time'
    )


@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    form = forms.BusShiftForm
    list_display = (
        'pk', 'bus', 'driver', 'departure_time', 'arrival_time', 'total_time'
    )
    fields = (
       'bus', 'driver', 'stops', 'departure_time', 'arrival_time', 'total_time'
    )
    readonly_fields = ('departure_time', 'arrival_time', 'total_time')
