import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.timezone import now, timedelta

from padam_django.apps.fleet.models import Driver, Bus, BusStop, BusShift
from padam_django.apps.geography.models import Place

User = get_user_model()

@pytest.fixture
def test_user():
    return User.objects.create(username='testuser', password='password')

@pytest.fixture
def test_bus():
    return Bus.objects.create(licence_plate='ABC1234')

@pytest.fixture
def test_place():
    return Place.objects.create(name='Test Place', longitude=0.0, latitude=0.0)

@pytest.fixture
def test_bus_stop(test_place):
    return BusStop.objects.create(name='Test Stop', place=test_place, arrival_time=now(), departure_time=now() + timedelta(hours=1))

@pytest.fixture
def test_driver(test_user):
    return Driver.objects.create(user=test_user)

@pytest.fixture
def test_bus_shift(test_bus, test_driver, test_place):
    bus_shift = BusShift.objects.create(bus=test_bus, driver=test_driver)
    bus_stop1 = BusStop.objects.create(name='Stop 1', place=test_place, departure_time=now())
    bus_stop2 = BusStop.objects.create(name='Stop 2', place=test_place, arrival_time=now() + timedelta(hours=1))
    bus_shift.stops.add(bus_stop1, bus_stop2)
    return bus_shift

@pytest.mark.django_db
def test_driver_string_representation(test_user):
    driver = Driver.objects.create(user=test_user)
    assert str(driver) == f"Driver: {test_user.username} (id: {driver.pk})"

@pytest.mark.django_db
def test_bus_string_representation(test_bus):
    assert str(test_bus) == f"Bus: {test_bus.licence_plate} (id: {test_bus.pk})"

@pytest.mark.django_db
def test_bus_stop_string_representation(test_bus_stop):
    assert str(test_bus_stop) == test_bus_stop.name

@pytest.mark.django_db
def test_bus_stop_clean_method_valid(test_bus_stop):
    try:
        test_bus_stop.clean()
    except ValidationError:
        pytest.fail('clean() raised ValidationError unexpectedly!')

@pytest.mark.django_db
def test_bus_stop_clean_method_no_times(test_place):
    bus_stop = BusStop(name='Invalid Stop', place=test_place)
    with pytest.raises(ValidationError):
        bus_stop.clean()

@pytest.mark.django_db
def test_bus_shift_start_time(test_bus_shift):
    assert test_bus_shift.start_time == test_bus_shift.stops.first().departure_time

@pytest.mark.django_db
def test_bus_shift_end_time(test_bus_shift):
    assert test_bus_shift.end_time == test_bus_shift.stops.last().arrival_time

@pytest.mark.django_db
def test_bus_shift_total_duration(test_bus_shift):
    expected_duration = test_bus_shift.stops.last().arrival_time - test_bus_shift.stops.first().departure_time
    assert test_bus_shift.total_duration == expected_duration
