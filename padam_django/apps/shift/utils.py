from datetime import datetime

from django.db.models import QuerySet
from django.core.exceptions import ValidationError
from padam_django.apps.shift.models import BusShift


def check_overlap(instance_departure: str, instance_arrival: str, plannings: QuerySet) -> bool:
    """Check if the travel times overlap for the bus or the driver.
        Return True if it is.
    """

    for planning in plannings:
        if (
            planning.departure_time.transit_time
            <= instance_departure
            <= planning.arrival_time.transit_time
            or planning.departure_time.transit_time
            <= instance_arrival
            <= planning.arrival_time.transit_time
        ):
            return True
    return False
