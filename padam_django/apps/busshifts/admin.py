from django.contrib import admin

# Register your models here.
from padam_django.apps.busshifts.models import BusStop, BusShift


class BusStopInline(admin.TabularInline):
    model = BusStop


class BusShiftAdmin(admin.ModelAdmin):
    inlines = [BusStopInline]


admin.site.register(BusShift, BusShiftAdmin)
admin.site.register(BusStop)
