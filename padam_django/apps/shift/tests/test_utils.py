from datetime import datetime

from django.test import TestCase

from padam_django.apps.shift.factories import (
    BusShiftFactory,
    BusStopTimeFactory,
)
from padam_django.apps.fleet.factories import DriverFactory
from padam_django.apps.shift.utils import check_overlap


class UtilsTest(TestCase):
    def setUp(self):
        self.departure_time = BusStopTimeFactory(transit_time="10:00:00")
        self.arrival_time = BusStopTimeFactory(transit_time="16:00:00")
        self.driver = DriverFactory(user__username="marshallmather")
        self.bus_shift = BusShiftFactory(
            arrival_time=self.arrival_time,
            departure_time=self.departure_time,
            driver=self.driver,
        )

    def test_check_overlap_true(self):
        departure_time = BusStopTimeFactory(transit_time="14:00:00")
        arrival_time = BusStopTimeFactory(transit_time="17:00:00")
        bus_shift = BusShiftFactory(
            arrival_time=arrival_time,
            departure_time=departure_time,
            driver=self.driver,
        )

        driver_shifts = self.driver.shifts_driver.exclude(pk=bus_shift.id)
        departure = datetime.strptime(
            bus_shift.departure_time.transit_time, "%H:%M:%S"
        ).time()
        arrival = datetime.strptime(
            bus_shift.departure_time.transit_time, "%H:%M:%S"
        ).time()

        self.assertTrue(check_overlap(departure, arrival, driver_shifts))

    def test_check_overlap_false(self):
        departure_time = BusStopTimeFactory(transit_time="16:30:00")
        arrival_time = BusStopTimeFactory(transit_time="18:00:00")
        bus_shift = BusShiftFactory(
            arrival_time=arrival_time,
            departure_time=departure_time,
            driver=self.driver,
        )

        driver_shifts = self.driver.shifts_driver.exclude(pk=bus_shift.id)
        departure = datetime.strptime(
            bus_shift.departure_time.transit_time, "%H:%M:%S"
        ).time()
        arrival = datetime.strptime(
            bus_shift.departure_time.transit_time, "%H:%M:%S"
        ).time()

        self.assertFalse(check_overlap(departure, arrival, driver_shifts))
