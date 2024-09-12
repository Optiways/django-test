from django.contrib import admin

from padam_django.apps.shift.models import BusShift, BusStop
from padam_django.apps.shift.admin.inlines import BusStopInline


@admin.register(BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    inlines = [BusStopInline]
    list_display = [
        'bus', 'driver', 'start_date', 'end_date', 'shift_time', 'stops_count'
    ]
    fields = [
        'bus', 'driver', 'start_date', 'end_date', 'shift_time', 'stops_count'
    ]
    readonly_fields = ['start_date', 'end_date', 'shift_time', 'stops_count']
    list_filter = ['bus', 'driver']

    def get_queryset(self, request):
        """Prevent duplicates queries on admin list page"""
        return super().get_queryset(
            request
        ).prefetch_related('stops').select_related('driver', 'bus')


@admin.register(BusStop)
class BusStopAdmin(admin.ModelAdmin):
    pass
