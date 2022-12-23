from __future__ import annotations

import typing

from django.core.exceptions import ValidationError
from django.forms import ModelForm

from padam_django.apps.fleet.models import BusShift

if typing.TYPE_CHECKING:
    from django.db.models.query import QuerySet


class BusShiftForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = BusShift

    def clean(self):
        self._validate_stops()
        self._validate_bus()
        self._validate_driver()

    def _max_shift(self):
        """Return end time of shift"""
        return max(self.cleaned_data["stops"].values_list('schedule'))[0]

    def _min_shift(self):
        """Return start time of shift"""
        return min(self.cleaned_data["stops"].values_list('schedule'))[0]

    def _validate_bus(self):
        """Check if the bus is free for the shift"""
        stored_bus_shift: QuerySet = BusShift.objects.filter(
            bus__pk=self.cleaned_data["bus"].pk,
            stops__schedule__range=[self._min_shift(), self._max_shift()]
        )
        if stored_bus_shift:
            raise ValidationError("This bus is already affected to another shift during this period")

    def _validate_driver(self):
        """Check if the driver is free for the shift"""
        stored_driver_shift: QuerySet = BusShift.objects.filter(
            driver__pk=self.cleaned_data["driver"].pk,
            stops__schedule__range=[self._min_shift(), self._max_shift()]
        )
        if stored_driver_shift:
            raise ValidationError("This driver is already affected to another shift during this period")

    def _validate_stops(self):
        """Validate stop minimal count"""
        if len(self.cleaned_data["stops"]) < 2:
            raise ValidationError("A Shift must have at least 2 stops")
