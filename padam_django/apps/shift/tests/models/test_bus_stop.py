from django.test import TestCase

from padam_django.apps.shift.factories import BusStopFactory


class BusStopTests(TestCase):
    def setUp(self):
        self.bus_stop = BusStopFactory()

    def test_bus_stop_str(self):
        bus_stop_name = self.bus_stop.name
        self.assertEqual(str(self.bus_stop), f"Bus stop: {bus_stop_name}")
