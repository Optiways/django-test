from datetime import datetime

from django.test import TestCase

from padam_django.apps.shift.factories import BusShiftFactory, BusStopFactory


class BusShiftTest(TestCase):
    def setUp(self):
        self.bus_stops = BusStopFactory.create_batch(size=3)
        self.bus_shift = BusShiftFactory(bus_stops=self.bus_stops)

    def test_bus_shift_str(self):
        bus_driver = self.bus_shift.driver.user.username
        bus_departure_time = self.bus_shift.departure_time.transit_time
        bus_arrival_time = self.bus_shift.arrival_time.transit_time

        self.assertEqual(str(self.bus_shift), "Bus shift:"
            f" {bus_driver} {bus_departure_time}"
            f"-{bus_arrival_time}")

    def test_departure_stop_name(self):
        departure_name = self.bus_shift.departure_time.stop.name

        self.assertEqual(self.bus_shift.departure_time.stop.name, departure_name)

    def test_arrival_stop_name(self):
        arrival_name = self.bus_shift.arrival_time.stop.name

        self.assertEqual(self.bus_shift.arrival_time.stop.name, arrival_name)

    def test_total_shift_time(self):
        total_shift = self.bus_shift.total_shift_time()
        elapse_time = datetime.strptime(
            self.bus_shift.arrival_time.transit_time, "%H:%M:%S"
        ) - datetime.strptime(self.bus_shift.departure_time.transit_time, "%H:%M:%S")

        result = round(elapse_time.total_seconds() / 60)

        self.assertEqual(result, total_shift)
