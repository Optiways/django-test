from datetime import time
from django.test import TestCase

from padam_django.apps.fleet.factories import BusShiftFactory, BusFactory, DriverFactory


class TestBusShiftModel(TestCase):
    def setUp(self) -> None:
        departure_time = time(hour=14, minute=0)
        arrival_time = time(hour=21, minute=0)
        self.bus_shift = BusShiftFactory(
            driver=DriverFactory(),
            bus=BusFactory(),
            departure_time=departure_time,
            arrival_time=arrival_time,
        )

    def test_bus_shift_duration(self):
        assert self.bus_shift.duration == "07h00"
