from django.contrib import admin

from padam_django.apps.shift.forms import ScheduleStopForm

from .models import BusShift, BusStop, ScheduleStop


@admin.register(BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    # Make field not last stop, first_stop not editable
    readonly_fields = ("first_stop", "last_stop")
    list_display = (
        "bus",
        "driver",
        "get_stop_count",
        "get_validation_stop_information",
    )

    @admin.display(description="Stop count")
    def get_stop_count(self, obj):
        return ScheduleStop.objects.filter(bus_shift=obj.id).count()

    @admin.display(description="Stop count validation")
    def get_validation_stop_information(self, obj):
        stop_count = ScheduleStop.objects.filter(bus_shift=obj.id).count()
        if stop_count < 2:
            return "Missing bus stops"
        return "Valid bus stops count"


@admin.register(BusStop)
class BusStopAdmin(admin.ModelAdmin):
    pass


@admin.register(ScheduleStop)
class ScheduleStopAdmin(admin.ModelAdmin):
    form = ScheduleStopForm
