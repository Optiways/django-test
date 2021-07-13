from django.contrib import admin

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_driver')

    def is_driver(self, obj):
        return obj.is_driver
    is_driver.boolean = True
    is_driver.short_description = 'Is driver'
