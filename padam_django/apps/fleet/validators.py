
# Sys import.
import datetime
from re import A

# Django import.
from django.conf import settings
from django import forms

# App import
from .models import BusShift
from .utils import is_time_stop_between_existing_shift


def is_bus_shift_slot_valid(driver, bus, new_departure, new_arrival):
    """ Verify bus and driver shift overlap

    Args:
        departure (_type_, optional): time of shift departure. Defaults to departure.
        arrival (_type_, optional): time of shift arrival. Defaults to arrival.
    """
    
    print('is_time_slot_valid')

    travel_time = new_arrival - new_departure
    # Check departure and arrival coherence (+ delay) 
    if travel_time < datetime.timedelta(seconds=0, minutes=settings.BUS_SHIFT_MINUTES_INTERVAL):
        raise forms.ValidationError('Departure or arrival are to close!')

    # Get bus and driver shift
    driver_shift = BusShift.objects.filter(driver_id=driver)
    bus_shift = BusShift.objects.filter(bus_id=bus)

    # Combine driver and bus shift query
    registered_shifts = driver_shift | bus_shift
    print('registered_shifts', registered_shifts)
    
    # verify if new_departure > departure

    # verify if new_departure > departure AND new_departure < arrival
    registered_bus_shift = registered_shifts.filter(departure__lt=new_departure, arrival__gt=new_departure).order_by('departure')
    print('registered_bus_shift', registered_bus_shift)
    # verify if new_arrival > departure AND new_arrival < arrival
    registered_bus_shift = registered_shifts.filter(arrival__gt=new_arrival, departure__lt=new_arrival).order_by('departure')
    print('registered_bus_shift', registered_bus_shift)    
    
    overlap_shift = registered_bus_shift.exists()
    print('overlap shift=', overlap_shift)
    if overlap_shift:
        err = 'This bus or this driver is already busy!'
        raise forms.ValidationError(err)


def is_bus_time_stop_slot_valid(driver, bus, new_time_stop):
    """ Verify bus and driver shift overlap

    Args:
        departure (_type_, optional): time of shift departure. Defaults to departure.
        arrival (_type_, optional): time of shift arrival. Defaults to arrival.
    """
    # Get all BusShifts
    Q = BusShift.objects.all()
    is_time_stop_between_existing_shift(Q, new_time_stop, driver, bus)

    # Get all bus and driver shift
    # driver_shift = BusShift.objects.filter(driver_id=driver)
    # bus_shift = BusShift.objects.filter(bus_id=bus)
    
    # Combine driver and bus shift query
    # registered_shifts = driver_shift | bus_shift
    
    # Get all rides in ascendant order
    # registered_shifts.order_by('departure')

    # verify if new_time_stop > departure AND new_time_stop < arrival


