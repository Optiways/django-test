from django.test import TestCase
from .models import BusShift, BusStop
from padam_django.apps.geography.models import Place
from padam_django.apps.fleet.models import Bus, Driver
from datetime import datetime, timedelta
from padam_django.apps.users.models import User
from django.utils import timezone
from .utils import is_driver_possible, is_bus_possible


class BusShiftTestCase(TestCase):
    def setUp(self):
        self.today = datetime.now(tz=timezone.utc)
        self.delta = timedelta(hours=3)

        self.bus1 = Bus.objects.create(licence_plate="AA 1234 AB")
        self.bus2 = Bus.objects.create(licence_plate="AB 5678 BC")

        self.user1 = User.objects.create(username="Driver 1", email="driver1@padam.io",
                                         first_name="Drive", last_name="In")
        self.user2 = User.objects.create(username="Driver 2", email="driver2@padam.io",
                                         first_name="Mc", last_name="Drive")

        self.driver1 = Driver.objects.create(user=self.user1)
        self.driver2 = Driver.objects.create(user=self.user2)

        self.place1 = Place.objects.create(name="Place 1", longitude=0.1001, latitude=0.2002)
        self.place2 = Place.objects.create(name="Place 2", longitude=0.2001, latitude=0.3002)
        self.place3 = Place.objects.create(name="Place 1", longitude=0.3001, latitude=0.4002)
        self.place4 = Place.objects.create(name="Place 2", longitude=0.4001, latitude=0.5002)

        self.bus_stop1 = BusStop.objects.create(name="Bus Stop 1", place=self.place1, stop_datetime=self.today)
        self.bus_stop2 = BusStop.objects.create(name="Bus Stop 2", place=self.place2,
                                                stop_datetime=self.today + self.delta)
        self.bus_stop3 = BusStop.objects.create(name="Bus Stop 3", place=self.place3,
                                                stop_datetime=self.today + timedelta(days=1))
        self.bus_stop4 = BusStop.objects.create(name="Bus Stop 4", place=self.place4,
                                                stop_datetime=self.today + self.delta + timedelta(days=1))

        self.bus_shift1 = BusShift.objects.create(bus=self.bus1, driver=self.driver1)
        self.bus_shift1.bus_stops.add(self.bus_stop1, self.bus_stop2)

        self.bus_shift2 = BusShift.objects.create(bus=self.bus2, driver=self.driver2)
        self.bus_shift2.bus_stops.add(self.bus_stop3, self.bus_stop4)

    def test_get_shift_duration(self):
        self.assertEqual(self.bus_shift1.get_bus_shift_duration.seconds, self.delta.seconds)

    def test_is_driver_possible(self):
        self.assertFalse(is_driver_possible(self.driver1, self.bus_shift1.bus_stops))
        self.assertTrue(is_driver_possible(self.driver1, self.bus_shift2.bus_stops))

    def test_is_bus_possible(self):
        self.assertFalse(is_driver_possible(self.driver1, self.bus_shift1.bus_stops))
        self.assertTrue(is_driver_possible(self.driver1, self.bus_shift2.bus_stops))
