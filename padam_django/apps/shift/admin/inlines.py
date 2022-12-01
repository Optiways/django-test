from django.contrib import admin

from padam_django.apps.shift.models import BusStop


__all__ = ['BusStopInline']


class BusStopInline(admin.TabularInline):
    model = BusStop
    extra = 1

