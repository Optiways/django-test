from django.contrib import admin
from django.core.exceptions import ValidationError

from django import forms

from .models import BusStop, BusStopTime, BusShift


class BusShiftForm(forms.ModelForm):
    def clean(self):
        bus_stops = self.cleaned_data.get("bus_stops")

        if bus_stops:
            if bus_stops.count() < 2:
                raise ValidationError("Need at least 2 bus stops.")


@admin.register(BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    list_display = ("bus", "driver", "departure_time", "arrival_time")
    list_filter = (
        "bus",
        "driver",
    )
    ordering = ("-pk",)
    form = BusShiftForm

    fieldsets = (
        ("Fleet informations", {"fields": ("driver", "bus")}),
        (
            "Time informations",
            {
                "fields": ("departure_time", "arrival_time"),
            },
        ),
        (
            "Stop informations",
            {
                "fields": ("bus_stops",),
            },
        ),
    )


@admin.register(BusStopTime)
class BusStopTimeAdmin(admin.ModelAdmin):
    list_display = ("transit_time", "stop")
    ordering = ("-pk",)


@admin.register(BusStop)
class BusStopAdmin(admin.ModelAdmin):
    list_display = ("name", "location")
    ordering = ("-pk",)
