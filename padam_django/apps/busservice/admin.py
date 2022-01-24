from django.contrib import admin
from . import models


@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    list_display = ("bus", "driver", "start_time", "end_time")
    pass


@admin.register(models.BusStop)
class BusStopAdmin(admin.ModelAdmin):
    list_display = ("place", "timestamp", "busshift")
    pass
