from datetime import datetime, timedelta

from django.test import TestCase
from django.utils.timezone import utc

from padam_django.apps.fleet.models import Bus, Driver
from padam_django.apps.geography.models import Place
from padam_django.apps.ride.models import BusStop, BusShift, BusSubRoute
from padam_django.apps.ride.queries import is_driver_available, is_bus_available
from padam_django.apps.users.models import User


class BusShiftTest(TestCase):

    def setUp(self):
        self.bus = Bus.objects.create(licence_plate="12345-abc")
        self.user = User.objects.create(email="test@test.com", username="test", password="testtesttest")
        self.driver = Driver.objects.create(user=self.user)
        self.place = Place.objects.create(name="rue du test", longitude=12.2, latitude=14.4)
        self.place2 = Place.objects.create(name="rue du test 2", longitude=12.3, latitude=14.5)
        self.bus_stop = BusStop.objects.create(stop_location=self.place)
        self.bus_stop2 = BusStop.objects.create(stop_location=self.place2)
        self.bus_shift = BusShift.objects.create(bus=self.bus, driver=self.driver)
        self.bus_shift2 = BusShift.objects.create(bus=self.bus, driver=self.driver)
        self.delta_time = timedelta(minutes=15)
        self.bus_sub_route = BusSubRoute.objects.create(bus_shift=self.bus_shift, bus_stop=self.bus_stop,
                                                        passage_datetime=datetime.now())
        self.bus_sub_route = BusSubRoute.objects.create(bus_shift=self.bus_shift, bus_stop=self.bus_stop2,
                                                        passage_datetime=datetime.now() + self.delta_time)
        self.bus_shift.set_departure_time()
        self.bus_shift.set_arrival_time()
        self.bus_shift.set_is_completed()
        self.bus_shift2.set_is_completed()

    def test_get_shift_duration(self):
        self.assertEqual(self.bus_shift.get_shift_duration().seconds, self.delta_time.seconds)

    def test_get_number_of_stop(self):
        self.assertEqual(self.bus_shift.get_number_of_stop(), 2)
        self.assertEqual(self.bus_shift2.get_number_of_stop(), 0)

    def test_is_completed(self):
        self.assertTrue(self.bus_shift.is_completed)
        self.assertFalse(self.bus_shift2.is_completed)

    def test_available_driver(self):  # todo : fix is_driver_available_method
        self.assertFalse(is_driver_available(self.driver.pk, utc.localize(datetime.now()), utc.localize(datetime.now() + self.delta_time)))
        self.assertTrue(is_driver_available(self.driver.pk, utc.localize(datetime.now() - self.delta_time), utc.localize(datetime.now())))

    def test_available_bus(self):  # todo : fix is_driver_available_method
        self.assertFalse(is_bus_available(self.bus.pk, utc.localize(datetime.now()), utc.localize(datetime.now() + self.delta_time)))
        self.assertTrue(is_bus_available(self.bus.pk, utc.localize(datetime.now() - self.delta_time), utc.localize(datetime.now())))