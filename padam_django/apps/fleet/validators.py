# Sys import.
import datetime

# App import
from django.conf import settings
from .models import BusShift
from .utils import is_time_stop_between_existing_shift


def is_bus_time_stop_slot_valid(driver, bus, new_time_stop):
    """ Check if bus time slot is valid

    Args:
        driver (str): 
            Bus driver we want the shifts to be filtered

        bus (str): 
            Driver bus we want the shifts to be filtered

        new_time_stop (models.DateTimeField):
            Time stop we want to valid
    
    Returns:
        Boolean: Time slot validation
    """
    # Get all BusShifts of same input time stop date
    date_bus_shift_qs = BusShift.objects.filter(
        date=new_time_stop.date(),
    )

    if is_time_stop_between_existing_shift(date_bus_shift_qs, driver, bus, new_time_stop):
        return True
    else:
        return False   