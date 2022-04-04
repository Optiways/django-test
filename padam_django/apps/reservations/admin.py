from django.contrib import admin

from .models import BusShift, BusStop


class BusStopInline(admin.StackedInline):
    model = BusStop


class BusShiftAdmin(admin.ModelAdmin):
    inlines = [BusStopInline,]


admin.site.register(BusShift, BusShiftAdmin)