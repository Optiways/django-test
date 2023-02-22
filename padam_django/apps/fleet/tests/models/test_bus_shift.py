from datetime import time

from django.core.exceptions import ValidationError
from django.test import TestCase

from padam_django.apps.fleet.factories import BusShiftFactory, BusFactory, DriverFactory
from padam_django.apps.fleet.models import BusShift


class TestBusShiftModel(TestCase):
    def setUp(self) -> None:
        departure_time = time(hour=14, minute=0)
        arrival_time = time(hour=21, minute=0)
        self.bus = BusFactory()
        self.driver = DriverFactory()
        self.bus_shift = BusShiftFactory(
            driver=self.driver,
            bus=self.bus,
            departure_time=departure_time,
            arrival_time=arrival_time,
        )

    def test_bus_shift_duration(self):
        assert self.bus_shift.duration == "07h00"

    def test_bus_shift_save_with_busy_driver(self):
        departure_time = time(hour=15, minute=0)
        arrival_time = time(hour=16, minute=0)

        self.assertEqual(BusShift.objects.count(), 1)

        with self.assertRaises(ValidationError):
            BusShiftFactory(
                driver=self.driver, departure_time=departure_time, arrival_time=arrival_time
            )

        self.assertEqual(BusShift.objects.count(), 1)

    def test_bus_shift_save_with_free_driver(self):
        departure_time = time(hour=7, minute=0)
        arrival_time = time(hour=8, minute=0)

        self.assertEqual(BusShift.objects.count(), 1)

        BusShiftFactory(
            driver=self.driver, departure_time=departure_time, arrival_time=arrival_time
        )

        self.assertEqual(BusShift.objects.count(), 2)

    def test_bus_shift_save_with_busy_bus(self):
        departure_time = time(hour=17, minute=0)
        arrival_time = time(hour=18, minute=0)

        self.assertEqual(BusShift.objects.count(), 1)

        with self.assertRaises(ValidationError):
            BusShiftFactory(bus=self.bus, departure_time=departure_time, arrival_time=arrival_time)

        self.assertEqual(BusShift.objects.count(), 1)

    def test_bus_shift_save_with_free_bus(self):
        departure_time = time(hour=9, minute=0)
        arrival_time = time(hour=10, minute=0)

        self.assertEqual(BusShift.objects.count(), 1)

        BusShiftFactory(bus=self.bus, departure_time=departure_time, arrival_time=arrival_time)

        self.assertEqual(BusShift.objects.count(), 2)
