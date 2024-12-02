from django.contrib import admin

from padam_django.apps.fleet import models
from padam_django.apps.fleet.admin.inlines import ScheduledStopInlineAdmin


@admin.register(models.Bus)
class BusAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Driver)
class DriverAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    list_display = ("pk", "bus", "driver", "departure", "arrival")
    fields = ("bus", "driver")
    inlines = (ScheduledStopInlineAdmin,)
