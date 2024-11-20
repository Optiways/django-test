
from django.contrib import admin
from django.core.exceptions import ValidationError
from padam_django.apps.pathing.forms.bus_stop_form import BusStopForm
from padam_django.apps.pathing.models.bus_shift import BusShift
from padam_django.apps.pathing.models.bus_stop import BusStop
from padam_django.apps.pathing.forms.bus_shift_form import BusShiftForm
from django.utils.timezone import now


@admin.register(BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    form = BusShiftForm
    list_display = ['bus', 'driver']

    def save_model(self, request, obj, form, change):
        bus_stops = form.cleaned_data.get('bus_stops')
        obj.save()
        for bus_stop in bus_stops:
            bus_stop.bus_shift = obj
            bus_stop.save()


@admin.register(BusStop)
class BusStopAdmin(admin.ModelAdmin):
    form = BusStopForm
