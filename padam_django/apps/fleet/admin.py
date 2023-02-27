from django import forms
from django.contrib import admin
from django.forms import ValidationError
from django.db.models import Q

from . import models


@admin.register(models.Bus)
class BusAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Driver)
class DriverAdmin(admin.ModelAdmin):
    pass


class BusStopInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        stops = [data for data in self.cleaned_data if data.get("time")]
        if len(stops) < 2:
            raise ValidationError("Shift should have at least 2 stops")
        else:
            end = max(
                stops,
                key=lambda x: x["time"],
            )["time"]
            start = min(stops, key=lambda x: x["time"])["time"]
            query = Q(time__lt=end)
            query.add(Q(time__gt=start), Q.AND)
            bus_already_used = (
                models.BusStop.objects.exclude(shift__id=self.instance.pk)
                .filter(shift__bus__pk=self.instance.bus_id)
                .filter(query)
            )
            driver_already_on_shift = (
                models.BusStop.objects.exclude(shift__id=self.instance.pk)
                .filter(shift__driver__pk=self.instance.driver_id)
                .filter(query)
            )
            if bus_already_used.count() > 0:
                raise ValidationError("Bus already used")
            if driver_already_on_shift.count() > 0:
                raise ValidationError(f"Driver alreay on shift")


class StopInline(admin.TabularInline):
    model = models.BusStop
    formset = BusStopInlineFormset


@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    inlines = [StopInline]
