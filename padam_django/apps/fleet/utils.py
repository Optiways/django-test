
from . import models
from django import forms

def update_fields_instance(instance, fields, save=False):
    [setattr(instance, key, val) for key, val in fields.items()]
    if save:
        instance.save()


def is_time_stop_between_existing_shift(Q, driver, bus, time_stop):
    # if driver busy
    Q1 = Q.filter(
        driver=driver,
        departure__date__gte=time_stop, 
        arrival__date__lte=time_stop
    )
    if Q1.exists():
        raise forms.ValidationError('Driver is already in shift')

    # is bus busy
    Q2 = Q.filter(
        # departure__day=time_stop,
        bus=bus,
        departure__date__gte=time_stop, 
        arrival__date__lte=time_stop
    )
    if Q2.exists():
        raise forms.ValidationError('Bus is already in shift')

    return True


def get_bus_shift_time(driver, bus):
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
    # If busstop instance uid doesn't exists create BusStop
    instance.bus_stop_id = instance.uid
    instance.departure = departure
    instance.arrival = arrival
    instance.travel_time = arrival - instance
    instance.save()

    return instance
