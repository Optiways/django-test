from django.contrib import admin

from . import models


@admin.register(models.Bus)
class BusAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Driver)
class DriverAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    list_array = ["bus", "driver"]
    list_display = list_array
    list_filter = list_array
    search_fields = list_array


@admin.register(models.BusStop)
class BusStopAdmin(admin.ModelAdmin):
    list_array = ["place"]
    list_display = list_array
    list_filter = list_array
    search_fields = list_array
