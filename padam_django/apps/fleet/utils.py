
from django import forms

from . import models

def is_time_stop_between_existing_shift(Q, driver, bus, time_stop):
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
    DriverExistingShifts = Q.filter(
        driver=driver,
        departure__date__gte=time_stop, 
        arrival__date__lte=time_stop
    )
    if DriverExistingShifts.exists():
        raise forms.ValidationError('Driver is already in shift')

    # is bus busy
    BusExistingShifts = Q.filter(
        bus=bus,
        departure__date__gte=time_stop, 
        arrival__date__lte=time_stop
    )
    if BusExistingShifts.exists():
        raise forms.ValidationError('Bus is already in shift')

    return True


def get_bus_shift_time(driver, bus):
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

    departure_model = models.BusStop.objects.filter(driver=driver, bus=bus).order_by('time_stop').first()
    if departure_model is not None:
        departure = departure_model.time_stop
        
    arrival_model = models.BusStop.objects.filter(driver=driver, bus=bus).order_by('time_stop').last()   
    if arrival_model is not None:
        arrival = arrival_model.time_stop

    if arrival is not None and departure is not None:
        travel_time = str(arrival - departure)

    print('shift time', travel_time)

    return departure, arrival, travel_time


def update_bus_shift(instance, departure, arrival):
    """ Update bus_shift attribute with shift time values and bus stop id

    Args:
        instance (Django Model): 
            Django Model instance to update

        departure (models.DateTimeField): 
            First stop of given shift instance

        arrival (models.DateTimeField): 
            Last stop of given shift instance

    Returns:
        Django Model instance: Django model instance updated and saved in database
    """
    instance.bus_stop_id = instance.uid
    instance.departure = departure
    instance.arrival = arrival
    instance.travel_time = arrival - instance
    instance.save()

    return instance


def update_instance_dict(instance, dict):
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
    print('dict', instance.__dict__)
    new_instance_dict = instance.__dict__.update(dict)
    print('new_dict', new_instance_dict)
    assert new_instance_dict is not None, "Error NullObject: Updated Form instance dict is null!"

    return new_instance_dict