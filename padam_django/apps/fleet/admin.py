from __future__ import annotations

import typing

from django.contrib import admin

from . import models

if typing.TYPE_CHECKING:
    import datetime


@admin.register(models.Bus)
class BusAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    list_display = ('bus', 'driver', 'departure_date', 'arrival_date', 'travel_time', 'stop_count')

    def departure_date(self, obj: models.BusShift) -> datetime:
        return obj.departure_date

    def arrival_date(self, obj: models.BusShift) -> datetime:
        return obj.departure_date

    def travel_time(self, obj: models.BusShift) -> datetime:
        return obj.travel_time

    def stop_count(self, obj: models.BusShift) -> int:
        return obj.stops.count()


@admin.register(models.BusStop)
class BusStopAdmin(admin.ModelAdmin):
    list_display = ('place', 'schedule')


@admin.register(models.Driver)
class DriverAdmin(admin.ModelAdmin):
    pass
