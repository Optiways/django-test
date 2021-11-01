from datetime import time
from django.db.models import QuerySet


def check_overlap(
    instance_departure: time, instance_arrival: time, plannings: QuerySet
) -> bool:
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
