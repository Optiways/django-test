from django.contrib import admin

from . import models


@admin.register(models.StartBusStop)
class StartBusStopAdmin(admin.ModelAdmin):
    pass


@admin.register(models.EndBusStop)
class EndBusStopAdmin(admin.ModelAdmin):
    pass
