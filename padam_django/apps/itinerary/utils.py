from .models import BusShift


def is_driver_possible(driver, bus_stops):
    for bus_shift in BusShift.objects.filter(driver__id=driver.id).order_by('bus_stops__stop_datetime'):
        if bus_shift.get_stop_datetime >= bus_stops.first().stop_datetime <= bus_shift.get_start_datetime \
                or bus_shift.get_stop_datetime >= bus_stops.last().stop_datetime >= bus_shift.get_start_datetime:
            return False
    return True


def is_bus_possible(bus, bus_stops):
    for bus_shift in BusShift.objects.filter(bus__id=bus.id).order_by('bus_stops__stop_datetime'):
        if bus_shift.get_stop_datetime >= bus_stops.first().stop_datetime <= bus_shift.get_start_datetime \
                or bus_shift.get_stop_datetime >= bus_stops.last().stop_datetime >= bus_shift.get_start_datetime:
            return False
    return True
