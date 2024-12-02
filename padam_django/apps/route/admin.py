from django.contrib import admin

from . import forms
from .models import BusShift, BusStop


@admin.register(BusStop)
class BusStopAdmin(admin.ModelAdmin):
    """
    Django Admin configuration for the `BusStop` model.

    The admin page displays a list of all the available bus stops, including their place name
    and transit time.
    """
    list_display = ('place', 'transit_time')


@admin.register(BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    """
    Django Admin configuration for the `BusShift` model.

    The admin page allows users to create, view, update, and delete instances of the `BusShift` model.
    The form used to create or update instances of the `BusShift` model is defined by the `BusShiftForm`
    class in the `forms` module.

    The list of `BusShift` instances includes the bus and driver assigned to each shift, as well as the
    departure time, arrival time, and duration of the shift. The `BusShift` form includes fields to
    specify the bus and driver, as well as a many-to-many relationship to the `BusStop` model to specify
    the stops on the route.

    The `departure_time`, `arrival_time`, and `shift_duration` fields are automatically calculated based 
    on the stops included in the shift.
    """
    form = forms.BusShiftForm
    list_display = ('bus', 'driver', 'departure_time', 'arrival_time', 'shift_duration')
    fields = ('bus', 'driver', 'stops')
