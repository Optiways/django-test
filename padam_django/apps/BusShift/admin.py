from django.contrib import admin

from . import models


@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    pass
