from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError

from . import models


@admin.register(models.BusStop)
class BusStopAdmin(admin.ModelAdmin):
    pass


class BusShiftAdminForm(forms.ModelForm):
    class Meta:
        model = models.BusShift
        fields = "__all__"

    #TODO: Form filtering to avoid seeing BusStops from all BusShifts

    def clean(self):
        """Validate that a single Bus or Driver cannot be assigned at
        the same time to several BusShifts.

        Raises:
            ValidationError: Field/description dict containing
            the violation error(s).
        """
        validation_errors = {}

        # Check that BusShift has at least 2 stops
        stops: list[models.BusStop] = self.cleaned_data.get("stops", [])
        stops_count = len(stops)
        if stops_count < 2:
            validation_errors["stops"] = (
                "BusShift must have at least two BusStops "
                f"({stops_count} found)."
            )

        # If no bus and no driver is set, no possible conflict
        if (
            self.cleaned_data.get("bus") is None
            and self.cleaned_data.get("driver") is None
        ):
            return
        # Check that BusShift is not overlapping with another shift
        for shift in models.BusShift.objects.all():
            if shift.pk == self.instance.pk or (
                shift.bus != self.cleaned_data.get("bus")
                and shift.driver != self.cleaned_data.get("driver")
            ):
                # It's the same shift, or both the bus and the driver differ
                continue
            if (
                shift.last_stop.date_time
                >= self.cleaned_data.get("stops").order_by("date_time").first().date_time
                and shift.first_stop.date_time
                <= self.cleaned_data.get("stops").order_by("date_time").last().date_time
            ):
                if shift.bus == self.cleaned_data.get("bus"):
                    validation_errors["bus"] = (
                        "Bus is not available at this time (conflicts with "
                        f"'{shift}')."
                    )
                if shift.driver == self.cleaned_data.get("driver"):
                    validation_errors["driver"] = (
                        f"{shift.driver} is not available at this time "
                        f"(conflicts with '{shift}')."
                    )

        if validation_errors:
            raise ValidationError(validation_errors)

        return self.cleaned_data


@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    # TODO: ordering (by first stop date_time)
    
    list_display = (
        "pk",
        "first_stop_date_time",
        "bus",
        "driver",
        "stops_count",
        "first_stop",
        "last_stop",
        # "is_valid",  # Not implemented yet
    )

    # def is_valid(self, obj):
    #     return obj.is_valid

    # is_valid.boolean = True
    # is_valid.short_description = "Is valid"

    form = BusShiftAdminForm
