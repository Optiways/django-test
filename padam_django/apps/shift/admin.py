from django.contrib import admin
from . import models

@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    list_display = ('id', 'bus', 'driver', 'departure_stop', 'arrival_stop')
    filter = ('bus', 'driver')
    ordering = ['bus', 'departure_stop']    

@admin.register(models.BusStop)
class BusStopAdmin(admin.ModelAdmin):
    pass

@admin.register(models.BusStopTime)
class BusStopTimeAdmin(admin.ModelAdmin):
    pass