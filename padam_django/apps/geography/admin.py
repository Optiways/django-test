from django.contrib import admin

from . import models


@admin.register(models.Place)
class PlaceAdmin(admin.ModelAdmin):
    pass

@admin.register(models.BusStop)
class BusStopAdmin(admin.ModelAdmin):
    pass

@admin.register(models.BusShift)
class BusSShiftAdmin(admin.ModelAdmin):
    pass
