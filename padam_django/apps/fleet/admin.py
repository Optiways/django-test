
# Django import.
from django.contrib import admin

# App import
from . import models
from .forms import BusShiftForm



@admin.register(models.BusStop)
class BusStopAdmin(admin.ModelAdmin):
    list_display = ('uid', 'driver', 'bus', 'arrival',)

@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    form = BusShiftForm
    list_display = ('uid', 'driver', 'bus', 'departure', 'arrival',)
    readonly_fields = ( 'travel_time', )

@admin.register(models.Bus)
class BusAdmin(admin.ModelAdmin):
    pass 
@admin.register(models.Driver)
class DriverAdmin(admin.ModelAdmin):
    pass
