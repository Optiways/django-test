from django.contrib import admin

from . import models


@admin.register(models.Place)
class PlaceAdmin(admin.ModelAdmin):
    pass

@admin.register(models.BusStop)
class BusStopAdmin(admin.ModelAdmin):
    pass

class BusLineStopInline(admin.TabularInline):
    model = models.BusLineStop
    extra = 0

@admin.register(models.BusLine)
class BusLineAdmin(admin.ModelAdmin):
    inlines = (BusLineStopInline,)
    pass
