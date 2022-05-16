from django.contrib import admin
from .models import BusStop, BusShift
from .forms import BusShiftForm


@admin.register(BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    form = BusShiftForm


@admin.register(BusStop)
class BusStopAdmin(admin.ModelAdmin):
    pass