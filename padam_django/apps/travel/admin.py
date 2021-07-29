from django.contrib import admin
from . import models

@admin.register(models.BusStop)
class BusStopAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    readonly_fields = ("departure_time", "arrival_time", "travel_time")


@admin.register(models.BusStopDate)
class BusStopDateAdmin(admin.ModelAdmin):
    pass
