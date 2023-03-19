from django.contrib import admin
from . import models


class BusStopInline(admin.TabularInline):
    model = models.BusStop
    min_num = 2  # a BusShift should get at least 2 BusStops
    extra = 0


@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    inlines = [BusStopInline]
