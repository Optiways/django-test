from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import BaseInlineFormSet

from . import models
from .utils import is_shifts_compatible
from ..journey.models import BusShift


@admin.register(models.Place)
class PlaceAdmin(admin.ModelAdmin):
    pass


class BusStopInlineFormSet(BaseInlineFormSet):

    def clean(self):
        # At least 2 bus stop should be associated
        if len(self.cleaned_data) < 2:
            raise ValidationError(
                f'Bus shift should contain at least 2 bus stop, it contains {len(self.cleaned_data)}.')

        ordered_bus_stops = sorted(self.cleaned_data, key=lambda bus_stop: bus_stop['pickup_time'])
        related_bus_shifts = BusShift.objects.filter(
            Q(bus_id=self.instance.bus.pk) | Q(driver_id=self.instance.driver.pk)
        ).exclude(pk=self.instance.pk)

        for bus_shift in related_bus_shifts:
            if not is_shifts_compatible(departure_shift_a=ordered_bus_stops[0]['pickup_time'],
                                        arrival_shift_a=ordered_bus_stops[-1]['pickup_time'],
                                        departure_shift_b=bus_shift.departure_time,
                                        arrival_shift_b=bus_shift.arrival_time):
                raise ValidationError(f'Bus shift cannot be created because it overrides shift {bus_shift}.')

        super().clean()


class BusStopInline(admin.StackedInline):
    model = models.BusStop
    formset = BusStopInlineFormSet
    extra = 0
