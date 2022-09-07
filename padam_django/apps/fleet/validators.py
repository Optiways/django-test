
# Sys import.
import datetime

# Django import.
from django.conf import settings
from django import forms

# App import
from .models import BusShift


def is_time_slot_valid(driver, bus, new_departure, new_arrival):
    """ Verify bus shift overlap

    Args:
        departure (_type_, optional): _description_. Defaults to departure.
        arrival (_type_, optional): _description_. Defaults to arrival.
    """

    # Check departure and arrival coherence (+ 5 minutes delay) 
    print(new_departure.minute, new_arrival.minute)
    
    if new_arrival - new_departure < datetime.timedelta(seconds=0, minutes=settings.BUSSHIFT_MINUTES_INTERVAL):
        raise forms.ValidationError('Departure or arrival are to close!')

    # For each BusShift verify if new_departure > departure AND new_departure < arrival
    
    # Get driver shift
    driver_shift = BusShift.objects.filter(driver_id=driver)
    # Get bus shift
    bus_shift = BusShift.objects.filter(bus_id=bus)
    # Use Union
    registered_shifts = driver_shift | bus_shift
    print('registered_shifts', registered_shifts)
    registered_bus_shift = registered_shifts.filter(departure__gt=new_departure, arrival__lt=new_arrival).order_by('departure')
    print('registered_bus_shift', registered_bus_shift)
    overlap_shift1 = registered_bus_shift.exists()
    print('overlap shift1=', overlap_shift1)
    if overlap_shift1:
        err = 'This bus or the driver is already busy!'
        raise forms.ValidationError(err)

