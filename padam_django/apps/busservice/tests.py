from datetime import datetime, timezone, timedelta
import pytest
from padam_django.apps.busservice.models import BusShift
from padam_django.apps.busservice.factories import BusShiftFactory, BusStopFactory
from padam_django.apps.busservice.exceptions import BusOrDriverOccupiedError


@pytest.mark.django_db
def test_bushift_factory():
    BusShiftFactory()
    assert BusShift.objects.count() == 1


@pytest.mark.django_db
def test_bushift_get_start_time():
    busshift = BusShiftFactory()
    start_time = datetime.now(timezone.utc)
    BusStopFactory(busshift=busshift, timestamp=start_time)
    assert busshift.start_time == start_time


@pytest.mark.django_db
def test_bushift_get_end_time():
    busshift = BusShiftFactory()
    end_time = datetime.now(timezone.utc)
    BusStopFactory(busshift=busshift, timestamp=end_time)
    assert busshift.end_time == end_time


@pytest.mark.django_db
def test_bushift_get_end_time():
    busshift = BusShiftFactory()
    end_time = datetime.now(timezone.utc)
    BusStopFactory(busshift=busshift, timestamp=end_time)
    assert busshift.end_time == end_time


@pytest.mark.django_db
def test_is_during_busshift():
    busshift = BusShiftFactory()
    start_time = datetime.now(timezone.utc)
    in_between_time = start_time + timedelta(hours=2)
    end_time = start_time + timedelta(hours=3)
    BusStopFactory(busshift=busshift, timestamp=start_time)
    in_between_busstop = BusStopFactory(busshift=busshift, timestamp=in_between_time)
    BusStopFactory(busshift=busshift, timestamp=end_time)
    assert busshift.is_during_shift(in_between_busstop.timestamp) == True


@pytest.mark.django_db
def test_busstop_is_overlapping():
    busshift = BusShiftFactory()
    another_busshift_same_driver = BusShiftFactory(driver=busshift.driver)
    another_busshift_same_bus = BusShiftFactory(bus=busshift.bus)
    start_time = datetime.now(timezone.utc)
    in_between_time = start_time + timedelta(hours=2)
    end_time = start_time + timedelta(hours=3)
    BusStopFactory(busshift=busshift, timestamp=start_time)
    BusStopFactory(busshift=busshift, timestamp=end_time)
    BusStopFactory(busshift=busshift, timestamp=in_between_time)
    with pytest.raises(BusOrDriverOccupiedError):
        BusStopFactory(busshift=another_busshift_same_driver, timestamp=in_between_time)

    with pytest.raises(BusOrDriverOccupiedError):
        BusStopFactory(busshift=another_busshift_same_bus, timestamp=in_between_time)
