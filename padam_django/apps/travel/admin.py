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


class StartBusStopForm(forms.ModelForm):
    class Meta:
        model = models.StartBusStop
        fields = (
            "user",
            "place",
            "ts_requested",
            "ts_estimated",
            "ts_boarded",
            "has_boarded",
        )


@admin.register(models.StartBusStop)
class StartBusStopAdmin(BusStopAdminMixin, admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
    ) + BusStopAdminMixin.list_display

    form = StartBusStopForm


class EndBusStopForm(forms.ModelForm):
    class Meta:
        model = models.EndBusStop
        fields = (
            "start",
            "place",
            "ts_requested",
            "ts_estimated",
            "ts_boarded",
            "has_boarded",
        )


@admin.register(models.EndBusStop)
class EndBusStopAdmin(BusStopAdminMixin, admin.ModelAdmin):
    list_display = (
        "pk",
        "start",
    ) + BusStopAdminMixin.list_display
    form = EndBusStopForm
