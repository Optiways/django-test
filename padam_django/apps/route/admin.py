from django.contrib import admin

from .forms import BusShiftForm
from .models import BusShift, BusStop, BusStopDate

@admin.register(BusStop)
class BusStopAdmin(admin.ModelAdmin):
    pass

@admin.register(BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    form = BusShiftForm

@admin.register(BusStopDate)
class BusStopDateAdmin(admin.ModelAdmin):
    pass
