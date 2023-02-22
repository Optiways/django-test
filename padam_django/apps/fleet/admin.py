from django.contrib import admin

from . import models


@admin.register(models.Bus)
class BusAdmin(admin.ModelAdmin):
    search_fields = ("licence_plate",)


@admin.register(models.Driver)
class DriverAdmin(admin.ModelAdmin):
    search_fields = ("user__username",)


@admin.register(models.BusStop)
class BusStopAdmin(admin.ModelAdmin):
    search_fields = ("place__name",)


@admin.register(models.BusShift)
class BusShitAdmin(admin.ModelAdmin):
    list_display = ("id", "bus", "driver", "total_stops", "departure_time", "arrival_time", "duration")
    list_filter = ("bus", "driver")
    search_fields = ("bus__licence_plate", "driver__user__username")
    autocomplete_fields = ("bus", "driver", "stops")

    def total_stops(self, obj):
        return obj.stops.count()
    
    total_stops.short_description = 'Stops'

