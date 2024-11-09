from django.contrib import admin
from .models import BusShift, BusStop, BusShiftStop
from .forms import BusShiftForm

# Register your models here.
@admin.register(BusShift)
class ShiftAdmin(admin.ModelAdmin):
    form = BusShiftForm


@admin.register(BusStop)
class StopsAdmin(admin.ModelAdmin):
    pass


@admin.register(BusShiftStop)
class ShiftStopsAdmin(admin.ModelAdmin):
    pass
