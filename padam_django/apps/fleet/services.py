from typing import Tuple
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta

from django.db import models

from padam_django.apps.fleet.models import Driver


def get_time_diff_between(time_field: time, time_field2: time) -> Tuple[int, int]:
    date_time = datetime.combine(date.today(), time_field)
    date_time2 = date_time.combine(date.today(), time_field2)
    diff_time = relativedelta(date_time2, date_time)
    return diff_time.hours, diff_time.minutes


def check_driver_availability(driver: Driver, departure_time: time, arrival_time: time):
    return not driver.shifts.filter(
        models.Q(departure_time__range=(departure_time, arrival_time))
        | models.Q(arrival_time__range=(departure_time, arrival_time))
        | models.Q(departure_time__lte=departure_time, arrival_time__gte=arrival_time)
    ).exists()


def check_bus_availability(bus: Driver, departure_time: time, arrival_time: time):
    return not bus.shifts.filter(
        models.Q(departure_time__range=(departure_time, arrival_time))
        | models.Q(arrival_time__range=(departure_time, arrival_time))
        | models.Q(departure_time__lte=departure_time, arrival_time__gte=arrival_time)
    ).exists()
