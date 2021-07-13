from django.contrib import admin

from . import models


@admin.register(models.Place)
class PlaceAdmin(admin.ModelAdmin):
    pass
