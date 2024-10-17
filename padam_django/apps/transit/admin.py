from django.contrib import admin
from .forms import BusShiftForm, BusShiftFormSet, BusStopForm
from .models import BusStop, BusShift
from datetime import datetime, timedelta


class BusStopInline(admin.TabularInline):
    model = BusStop
    form = BusStopForm
    formset = BusShiftFormSet
    extra = 0
    min_num = 2
    validate_min = True

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.order_by('transit_time')
        return queryset


@admin.register(BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    inlines = [BusStopInline]
    form = BusShiftForm
    list_display = ['bus', 'driver', 'departure_place', 'departure_time', 'arrival_place', 'arrival_time',
                    'shift_duration']
    search_fields = ['bus__licence_plate', 'driver__user__first_name', 'driver__user__last_name']
    list_filter = ['bus', 'driver']

    @staticmethod
    def departure_place(obj: BusShift) -> str:
        return obj.departure_stop

    @staticmethod
    def arrival_place(obj: BusShift) -> str:
        return obj.arrival_stop

    @staticmethod
    def departure_time(obj: BusShift) -> datetime:
        return obj.departure_time

    @staticmethod
    def arrival_time(obj: BusShift) -> datetime:
        return obj.arrival_time

    @staticmethod
    def shift_duration(obj: BusShift) -> timedelta:
        return obj.shift_duration
