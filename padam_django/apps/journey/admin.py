from django.contrib import admin

from . import models


@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BusStop)
class BusStopAdmin(admin.ModelAdmin):
    pass
