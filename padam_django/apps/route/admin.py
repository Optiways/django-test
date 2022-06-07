from django.contrib import admin
from padam_django.apps.route.models import BusStop, BusStopForm

from . import models


class BusStopInline(admin.TabularInline):
    model = BusStop
    extra = 1
    formset = BusStopForm

@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    inlines = (BusStopInline,)

@admin.register(models.BusStop)
class BusStopAdmin(admin.ModelAdmin):
    pass
