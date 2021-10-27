from django.db.models import QuerySet

from padam_django.apps.shift.models import BusShift


def check_overlap(instance: BusShift, plannings: QuerySet) -> bool:
    instance_departure = instance.departure_stop.transit_time
    instance_arrival = instance.arrival_stop.transit_time

    for planning in plannings:
        if (
            instance_departure
            <= planning.departure_stop.transit_time
            <= instance_arrival
            or instance_departure
            <= planning.arrival_stop.transit_time
            <= instance_arrival
        ):
            return True
    return False
