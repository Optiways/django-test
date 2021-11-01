from datetime import datetime

from django.test import TestCase

from padam_django.apps.shift.factories import BusShiftFactory, BusStopFactory, BusStopTimeFactory
from padam_django.apps.fleet.factories import DriverFactory
from padam_django.apps.shift.utils import check_overlap


class UtilsTest(TestCase):
    def setUp(self):
        self.departure_time = BusStopTimeFactory(transit_time='10:00')
        self.arrival_time = BusStopTimeFactory(transit_time='19:00')
        self.driver = DriverFactory(user__username="marshallmather")
        self.bus_shift = BusShiftFactory(arrival_time=self.arrival_time,
                                         departure_time=self.departure_time,
                                         driver=self.driver)

    def test_check_overlap_true(self):
        pass
        # TODO

    def test_check_overlap_false(self):
        pass
        # TODO
