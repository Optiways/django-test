from padam_django.apps.ride.models import BusShift


def is_driver_available(driver_id, datetime_from, datetime_to) -> bool:  # todo : missing case / unit test doesnt work
    rides = BusShift.objects.filter(deleted=False, is_completed=True, driver_id=driver_id)\
        .values("departure_time", "arrival_time")
    for ride in rides:
        if ride["departure_time"] <= datetime_from <= ride["arrival_time"] or ride["departure_time"] <= datetime_to <= ride["arrival_time"] or datetime_to <= ride["departure_time"] <= datetime_from or datetime_to <= ride["arrival_time"] <= datetime_from:
            return False
    return True


def is_bus_available(bus_id, datetime_from, datetime_to) -> bool:  # todo : missing case / unit test doesnt work
    rides = BusShift.objects.filter(deleted=False, is_completed=True, bus_id=bus_id)\
        .values("departure_time", "arrival_time")
    for ride in rides:
        if ride["departure_time"] <= datetime_from <= ride["arrival_time"] or ride["departure_time"] <= datetime_to <= ride["arrival_time"] or datetime_to <= ride["departure_time"] <= datetime_from or datetime_to <= ride["arrival_time"] <= datetime_from:
            return False
    return True