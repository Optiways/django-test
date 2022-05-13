from django.contrib import admin

from padam_django.apps.schedules.forms import BusShiftForm
from padam_django.apps.schedules.models import BusShift


class BusStopInline(admin.TabularInline):
    model = BusShift.stops.through
    min_num = 2


class BusShiftAdmin(admin.ModelAdmin):
    inlines = [
        BusStopInline,
    ]
    form = BusShiftForm


admin.site.register(BusShift, BusShiftAdmin)
