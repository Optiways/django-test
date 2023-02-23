from typing import Tuple, Optional
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta

from django.db import models

from padam_django.apps.fleet.models import Driver, Bus


def get_time_diff_between(time_field: time, time_field2: time) -> Tuple[int, int]:
    date_time = datetime.combine(date.today(), time_field)
    date_time2 = date_time.combine(date.today(), time_field2)
    diff_time = relativedelta(date_time2, date_time)
    return diff_time.hours, diff_time.minutes


def check_driver_availability(driver: Driver, departure_time: time, arrival_time: time, shift_pk: Optional[int] = None):
    """Check if driver is available on time range.
    :arg shift_pk: exclude this shift from the research
    """
    shifts = driver.shifts.exclude(pk=shift_pk) if shift_pk else driver.shifts
    return not shifts.filter(
        models.Q(departure_time__range=(departure_time, arrival_time))
        | models.Q(arrival_time__range=(departure_time, arrival_time))
        | models.Q(departure_time__lte=departure_time, arrival_time__gte=arrival_time)
    ).exists()


def check_bus_availability(bus: Bus, departure_time: time, arrival_time: time, shift_pk: Optional[int] = None):
    shifts = bus.shifts.exclude(pk=shift_pk) if shift_pk else bus.shifts
    return not shifts.filter(
        models.Q(departure_time__range=(departure_time, arrival_time))
        | models.Q(arrival_time__range=(departure_time, arrival_time))
        | models.Q(departure_time__lte=departure_time, arrival_time__gte=arrival_time)
    ).exists()
