from django.contrib import admin
from .forms import BusShiftForm

from . import models


@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    form = BusShiftForm
    exclude = ('first_stop', 'last_stop')


@admin.register(models.BusStop)
class BusStopAdmin(admin.ModelAdmin):
    pass
