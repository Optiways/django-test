from django.contrib import admin

from . import models

# Register your models here.
@admin.register(models.BusShift)
class PlaceAdmin(admin.ModelAdmin):
    form = models.BusShiftForm
    list_display = ['bus', 'driver', 'start_time', 'end_time', 'duration']