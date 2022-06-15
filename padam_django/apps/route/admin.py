from django.contrib import admin
from . import models
from .forms import BusShiftForm

# Register your models here.
@admin.register(models.BusStop)
class BusStopAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    form = BusShiftForm
