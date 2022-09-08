
# Sys import.
import datetime
from re import A

# Django import.
from django.conf import settings
# App import
from .models import BusShift
from .utils import is_time_stop_between_existing_shift


def is_bus_time_stop_slot_valid(driver, bus, new_time_stop):
    """ Verify bus and driver shift overlap

    Args:
        departure (_type_, optional): time of shift departure. Defaults to departure.
        arrival (_type_, optional): time of shift arrival. Defaults to arrival.
    """
    # Get all BusShifts
    Q = BusShift.objects.all()
    is_time_stop_between_existing_shift(Q, driver, bus, new_time_stop)

