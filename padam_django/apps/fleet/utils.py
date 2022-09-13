# System import.
from datetime import datetime

# Django import.
from django import forms

# App import
from . import models


def is_time_stop_between_existing_shift(qs, driver, bus, time_stop):
    """ Check if time stop are between exiting bus shifts or driver shifts

    Args:
        Q (QuerySet): 
            Database queryset input to filter

        driver (str): 
            Bus Driver we want the shifts filtered

        bus (str): 
            Driver bus we want the shifts filtered

        time_stop (models.DateTimeField): 
            Bus stop time form input to valid

    Raises:
        forms.ValidationError: 
            bus stop time between existing driver shifts ([departure, arrival])
        forms.ValidationError: 
            bus stop time between existing bus shifts ([departure, arrival])

    Returns:
        Boolean: Validation of the form
    """

    # if driver busy
    qs_driver_existing_shifts = qs.filter(
        driver=driver,
        departure__lte=time_stop, 
        arrival__gte=time_stop,
        # FIX: Bug allowing to choose same time for two time stop
        # departure__date__lte=str(time_stop.date), 
        # departure__hour__lte=str(time_stop.hour), 
        # departure__minute__lte=str(time_stop.minute), 
        # arrival__date__gte=str(time_stop.date),
        # arrival__hour__gte=str(time_stop.hour), 
        # arrival__minute__gte=str(time_stop.minute), 
    )
    if qs_driver_existing_shifts.exists():
        raise forms.ValidationError('Driver is already in shift at this time')

    # is bus busy
    qs_bus_existing_shifts = qs.filter(
        bus=bus,
        departure__lte=time_stop, 
        arrival__gte=time_stop
    )
    if qs_bus_existing_shifts.exists():
        raise forms.ValidationError('Bus is already in shift at this time')

    return True


def get_bus_shift_time(driver, bus, new_time_stop):
    """ Get shift departure and arrival time by ordering driver and bus BusStop instances

    Args:
        driver (str): 
            Bus driver we want to get shift time

        bus (str): 
            Driver bus we want get shift time

    Returns:
        tuple: Tuple with departure, arrival and travel time 
    """
    departure, arrival, travel_time = [None]*3

    departure_model = models.BusStop.objects.filter(driver=driver, bus=bus, time_stop__date=new_time_stop.date()).order_by('time_stop').first()
    if departure_model is not None:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
        if new_time_stop > departure_model.time_stop:
            departure = departure_model.time_stop
            arrival = new_time_stop
        else:
            departure = new_time_stop
            arrival = departure_model.time_stop
    else:
        departure = new_time_stop

    if arrival is not None and departure is not None:
        travel_time = str(arrival - departure)

    return departure, arrival, travel_time


def get_update_instance_dict(instance, input_dict):
    """ Get instance dict and update it with another dict

    Args:
        instance (Django model): 
            Source of dict to update

        dict (dict): 
            Dict we to update with

    Returns:
        dict: Instance dict updated with given dict
    """
    assert instance.__dict__ is not None, "Error NullObject: Form instance dict is null!"

    new_instance_dict = instance.__dict__.copy()
    new_instance_dict.update(input_dict)
    new_instance_dict.pop('_state')
    new_instance_dict.pop('time_stop')
    new_instance_dict.pop('uid')

    update_dict_valid = {k: v for k, v in new_instance_dict.items() if v is not None}

    return update_dict_valid