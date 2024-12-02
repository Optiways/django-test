from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from padam_django.apps.journey.models import BusStop, BusShift
from padam_django.apps.fleet.factories import BusFactory, DriverFactory
from padam_django.apps.geography.factories import PlaceFactory


def create_bus_stops(start, stop, bus_shift):
    for i in range(start, stop + 1):
        BusStop(
            bus_shift=bus_shift,
            place=PlaceFactory(),
            datetime=datetime(2022, 1, 1, i, 0, 0),
        ).save()


def create_bus_shift(bus, driver):
    bus = bus or BusFactory()
    driver = driver or DriverFactory()
    bus_shift = BusShift(bus=bus, driver=driver)
    bus_shift.save()
    return bus_shift


def create_journey(start, stop, bus=None, driver=None):
    bus_shift = create_bus_shift(bus, driver)
    create_bus_stops(start, stop, bus_shift)
    return bus_shift


class BusOverlappingTestCase(TestCase):
    def setUp(self):
        self.bus = BusFactory()

    def test_one_journey(self):
        create_journey(1, 10, self.bus)

    def test_two_journeys_with_no_bus_overlapping(self):
        create_journey(1, 3, self.bus)
        create_journey(4, 5, self.bus)

    def test_three_journeys_with_no_bus_overlapping(self):
        create_journey(1, 3, self.bus)
        create_journey(7, 8, self.bus)
        create_journey(4, 5, self.bus)

    def test_two_journeys_with_bus_overlapping(self):
        create_journey(1, 3, self.bus)
        bus_shift = create_journey(4, 5, self.bus)
        with self.assertRaises(ValidationError):
            create_bus_stops(2, 2, bus_shift)


class DriverOverlappingTestCase(TestCase):
    def setUp(self):
        self.driver = DriverFactory()

    def test_one_journey(self):
        create_journey(1, 10, driver=self.driver)

    def test_two_journeys_with_no_driver_overlapping(self):
        create_journey(1, 3, driver=self.driver)
        create_journey(4, 5, driver=self.driver)

    def test_three_journeys_with_no_driver_overlapping(self):
        create_journey(1, 3, driver=self.driver)
        create_journey(7, 8, driver=self.driver)
        create_journey(4, 5, driver=self.driver)

    def test_two_journeys_with_driver_overlapping(self):
        create_journey(1, 3, driver=self.driver)
        bus_shift = create_journey(4, 5, driver=self.driver)
        with self.assertRaises(ValidationError):
            create_bus_stops(2, 2, bus_shift)
