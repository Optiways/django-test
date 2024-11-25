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
        "get_shift_start_information",
        "get_shift_end_information",
        "get_shift_duration_information",
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

    @admin.display(description="Shift start")
    def get_shift_start_information(self, obj):
        return obj.first_stop

    @admin.display(description="Shift end")
    def get_shift_end_information(self, obj):
        return obj.last_stop

    @admin.display(description="Total duration (hours)")
    def get_shift_duration_information(self, obj):
        return obj.shift_duration


@admin.register(BusStop)
class BusStopAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "place")


@admin.register(ScheduleStop)
class ScheduleStopAdmin(admin.ModelAdmin):
    form = ScheduleStopForm
    list_display = (
        "bus_shift",
        "bus_stop",
        "arrival",
    )
