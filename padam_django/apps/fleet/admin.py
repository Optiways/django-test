
# Django import.
from django.contrib import admin
from django import forms

# App import
from django.conf import settings
from . import models
from .forms import BusStopForm
from .filters import bus_stop_filter_by, driver_filter_by

@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    list_display = ('uid', 'driver', 'bus', 'departure', 'arrival', 'travel_time')
    readonly_fields = ( 'travel_time', 'date', 'last_update')

    def get_queryset(self, request):
        """ Override: Filter all BusShift records by driver

        Returns:
            queryset: Queryset filtered
        """
        # Return only authenticated user queryset
        qs = super(BusShiftAdmin, self).get_queryset(request)

        if not settings.DEBUG and not request.user.is_admin:
            return qs.filter(driver__user=request.user)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        """ Override: Filter form choicefield by user and date

        Args:
            obj (ModelForm, optional): BusShiftForm instance. Defaults to None.

        Returns:
            ModelForm: New BusShiftForm instance
        """
        if obj is not None:
            # Only show bus stop user of the driver at the same date
            kwargs['form'] = bus_stop_filter_by(obj.driver, obj.date)
            super(BusShiftAdmin, self).get_form(request, obj, **kwargs)

            # If user not superuser don't allow user to choose another driver for his own shifts
            if not settings.DEBUG or not request.user.is_admin:
                kwargs['form'] = driver_filter_by(request.user)  

        return super(BusShiftAdmin, self).get_form(request, obj, **kwargs)
        

@admin.register(models.BusStop)
class BusStopAdmin(admin.ModelAdmin):
    form = BusStopForm
    list_display = ('uid', 'driver', 'bus', 'time_stop',)
    readonly_fields = ('date', 'last_update')
    
    # Filter all database records
    def get_queryset(self, request):
        """ Override: Filter all database records by driver if user

        Returns:
            queryset: Queryset filtered
        """
        # Return only authenticated user queryset
        qs = super(BusStopAdmin, self).get_queryset(request)
        if not settings.DEBUG and not request.user.is_admin:
            return qs.filter(driver__user=request.user)
        return qs

    def get_form(self, request, obj=None, **kwargs):
        """ Override: Filter form choicefield by user and date

        Args:
            obj (ModelForm, optional): BusStopForm instance. Defaults to None.

        Returns:
            ModelForm: New BusStopForm instance
        """
        if obj is not None:
            # Only show bus stop user of the driver at the same date
            kwargs['form'] = bus_stop_filter_by(obj.driver, obj.date)
            super(BusStopAdmin, self).get_form(request, obj, **kwargs)

            # If user not superuser don't allow user to choose another driver for his own shifts
            if not settings.DEBUG or not request.user.is_admin:
                kwargs['form'] = driver_filter_by(request.user)  

        return super(BusStopAdmin, self).get_form(request, obj, **kwargs)

@admin.register(models.Bus)
class BusAdmin(admin.ModelAdmin):
    pass 
@admin.register(models.Driver)
class DriverAdmin(admin.ModelAdmin):
    pass
