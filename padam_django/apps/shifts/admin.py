from django.contrib import admin
from .models import BusShift, BusStop
from .modelform import BusShiftForm


class BusStopAdmin(admin.ModelAdmin):
    """ Class to manage the BusStop model through Django admin """
    list_display = ('place', 'planned_time')



class BusShiftAdmin(admin.ModelAdmin):
    """ Class to manage the BusShift model through Django admin """
    form = BusShiftForm
    list_display = ('bus', 'driver', 'start_time', 'end_time', 'total_duration_seconds')


admin.site.register(BusShift, BusShiftAdmin)
admin.site.register(BusStop, BusStopAdmin)