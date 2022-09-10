
# Sys import.
import datetime

# Django import.
from django.conf import settings

# App import
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
    # Get all BusShifts
    Q = BusShift.objects.all()

    if is_time_stop_between_existing_shift(Q, driver, bus, new_time_stop):
        return True
    else:
        return False    