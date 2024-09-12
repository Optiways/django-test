from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from padam_django.apps.fleet.models import Bus, Driver
from padam_django.apps.geography.models import Place
from padam_django.apps.users.models import User
from padam_django.apps.shift.models import BusShift, BusStop


class BusShiftTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.bulk_create([
            User(username="user1"), User(username="user2"),
            User(username="user4"), User(username="user3"),
        ])
        Driver.objects.bulk_create([
            Driver(user_id=u.pk) for u in User.objects.all()
        ])
        Bus.objects.bulk_create([
            Bus(licence_plate="licence1"), Bus(licence_plate="licence2"),
            Bus(licence_plate="licence3"), Bus(licence_plate="licence4"),
        ])
        Place.objects.bulk_create([
            Place(name="name1", longitude=12.345678, latitude=23.456789),
            Place(name="name2", longitude=34.567891, latitude=45.678912),
            Place(name="name3", longitude=56.789123, latitude=67.891234),
            Place(name="name4", longitude=78.912345, latitude=89.123456),
        ])

    def test_good_shift(self):
        bus_shift = BusShift.objects.create(driver_id=1, bus_id=1)
        BusStop.objects.create(
            bus_shift=bus_shift, start_date=datetime(2022, 12, 1, 20, 10, 1),
            end_date=datetime(2022, 12, 1, 20, 12, 1), place_id=1
        )
        bus_stop = BusStop.objects.create(
            bus_shift=bus_shift,
            start_date=datetime(2022, 12, 1, 20, 15, 1),
            end_date=datetime(2022, 12, 1, 20, 16, 12), place_id=2
        )
        self.assertIsNone(bus_stop.clean())

    def test_wrong_start_date_and_end_date_on_same_stop(self):
        bus_shift = BusShift.objects.create(driver_id=2, bus_id=2)
        bus_stop = BusStop.objects.create(
            bus_shift=bus_shift,
            start_date=datetime(2022, 12, 1, 20, 14, 1),
            end_date=datetime(2022, 12, 1, 20, 10, 12), place_id=2
        )
        self.assertRaises(ValidationError, bus_stop.full_clean)

    def test_wrong_shifts_with_two_stop_on_same_times(self):
        bus_shift = BusShift.objects.create(driver_id=3, bus_id=3)
        BusStop.objects.create(
            bus_shift=bus_shift,
            start_date=datetime(2022, 12, 1, 20, 30, 1),
            end_date=datetime(2022, 12, 1, 20, 32, 12), place_id=2
        )
        bus_stop = BusStop.objects.create(
            bus_shift=bus_shift,
            start_date=datetime(2022, 12, 1, 20, 31, 1),
            end_date=datetime(2022, 12, 1, 20, 34, 12), place_id=2
        )
        self.assertRaises(ValidationError, bus_stop.full_clean)
