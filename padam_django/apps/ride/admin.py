from django.contrib import admin
from padam_django.apps.ride.models import BusStop, BusShift, BusSubRoute


class BarInline(admin.TabularInline):
    model = BusShift.bus_stops.through


class BusStopAdmin(admin.ModelAdmin):
    inlines = [
        BarInline,
    ]
    list_display = [
        "stop_location",
        "deleted"
    ]


class BusShiftAdmin(admin.ModelAdmin):
    list_display = [
        "bus",
        "driver",
        "deleted",
        "is_completed"
    ]


class BusSubRouteAdmin(admin.ModelAdmin):
    list_display = [
        "bus_stop",
        "bus_shift",
        "passage_datetime"
    ]


admin.site.register(BusStop, BusStopAdmin)
admin.site.register(BusShift, BusShiftAdmin)
admin.site.register(BusSubRoute, BusSubRouteAdmin)