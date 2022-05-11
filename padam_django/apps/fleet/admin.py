from django.contrib import admin

from . import models


@admin.register(models.Bus)
class BusAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Driver)
class DriverAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BusShift)
class BusAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BusStop)
class DriverAdmin(admin.ModelAdmin):
    pass
