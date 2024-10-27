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


@admin.register(models.StartBusStop)
class StartBusStopAdmin(BusStopAdminMixin, admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
    ) + BusStopAdminMixin.list_display

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
