import datetime

from django.test import TestCase
from django.utils import timezone

from padam_django.apps.shift.models import BusStopTime
from padam_django.apps.shift.factories import BusStopTimeFactory


class BusStopTests(TestCase):
    def setUp(self):
        self.bus_stop_time = BusStopTimeFactory()

    def test_bus_stop_str(self):
        transit_time = self.bus_stop_time.transit_time
        stop_name = self.bus_stop_time.stop.name

        self.assertEqual(str(self.bus_stop_time), f"Bus stop in {stop_name} at {transit_time}")
