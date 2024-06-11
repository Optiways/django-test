from django.contrib import admin

from padam_django.apps.fleet.forms import BusShiftForm

from . import models


@admin.register(models.Bus)
class BusAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Driver)
class DriverAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    form = BusShiftForm


@admin.register(models.BusStop)
class BusStopAdmin(admin.ModelAdmin):
    pass
