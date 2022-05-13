from django.contrib import admin

from padam_django.apps.schedules.forms import BusShiftForm
from padam_django.apps.schedules.models import BusShift


class BusStopInline(admin.TabularInline):
    model = BusShift.stops.through

class BusShiftAdmin(admin.ModelAdmin):
    inlines = [
        BusStopInline,
    ]
    form = BusShiftForm

admin.site.register(BusShift, BusShiftAdmin)
