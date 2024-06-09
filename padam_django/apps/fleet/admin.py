from django.contrib import admin

from . import models


@admin.register(models.Bus)
class BusAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Driver)
class DriverAdmin(admin.ModelAdmin):
    pass

@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    list_display = ('name', 'bus', 'driver')

@admin.register(models.BusStop)
class BusStopAdmin(admin.ModelAdmin):
    list_display = ('name', 'time', 'place', 'bus_shift')
