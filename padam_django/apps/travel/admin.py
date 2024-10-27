from django import forms
from django.contrib import admin

from . import models


class BusStopAdminMixin:
    list_display = ("place", "ts_requested", "has_boarded")
    readonly_fields = (
        "ts_estimated",
        "ts_boarded",
        "has_boarded",
    )


class BusStopFormMixin(forms.ModelForm):
    class Meta:
        fields = (
            "place",
            "ts_requested",
            "ts_estimated",
            "ts_boarded",
            "has_boarded",
        )


class StartBusStopForm(BusStopFormMixin):
    class Meta:
        model = models.StartBusStop
        fields = ("user",) + BusStopFormMixin.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].queryset = self.fields["user"].queryset.filter(
            driver__isnull=True
        )


@admin.register(models.StartBusStop)
class StartBusStopAdmin(BusStopAdminMixin, admin.ModelAdmin):
    list_display = (
        (
            "pk",
            "user",
        )
        + BusStopAdminMixin.list_display
        + ("end_bus_stops",)
    )

    form = StartBusStopForm


class EndBusStopForm(BusStopFormMixin):
    class Meta:
        model = models.EndBusStop
        fields = ("start",) + BusStopFormMixin.Meta.fields


@admin.register(models.EndBusStop)
class EndBusStopAdmin(BusStopAdminMixin, admin.ModelAdmin):
    list_display = (
        "pk",
        "start",
    ) + BusStopAdminMixin.list_display
    form = EndBusStopForm


class BusShiftForm(forms.ModelForm):
    stops = forms.ModelMultipleChoiceField(
        label="List of stops",
        help_text="Select any number of stops for this shift",
        queryset=models.EndBusStop.objects.filter(shift__isnull=True),
        required=True,
    )

    class Meta:
        model = models.BusShift
        fields = ("driver", "bus", "stops")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            end_bus_stops_qs = self.instance.end_bus_stops.all()
            self.fields["stops"].initial = end_bus_stops_qs
            self.fields["stops"].queryset = (
                self.fields["stops"].queryset | end_bus_stops_qs
            )

    def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        instance.save()
        self.cleaned_data["stops"].update(shift=instance)
        return instance


@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    list_display = ("pk", "driver", "bus", "shift_start", "shift_end", "shift_duration")
    form = BusShiftForm
