from django.test import TestCase
from django.utils import timezone
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from ..models import BusStop, BusShift
from ...geography.models import Place
from ...fleet.models import Bus, Driver
from ..forms import BusShiftForm 
from django.contrib.auth import get_user_model
from datetime import timedelta


class BusShiftModelTests(TestCase):

    def setUp(self):
        self.bus = Bus.objects.create(licence_plate="BUS1")
        self.driver = Driver.objects.create(user=self.create_user())
        self.place1 = Place.objects.create(name="Stop 1", longitude=0.0, latitude=0.0)
        self.place2 = Place.objects.create(name="Stop 2", longitude=0.1, latitude=0.1)
        self.stop_time1 = timezone.now()
        self.stop_time2 = self.stop_time1 + timedelta(minutes=10)

    def create_user(self):
        """Helper method to create a user for the driver."""
        User = get_user_model()
        return User.objects.create_user(username="driver_user", password="password")

    def test_create_bus_stop(self):
        """Test that a BusStop can be created successfully."""
        unique_place = Place.objects.create(name="Stop A Unique", longitude=0.2, latitude=0.2)
        bus_stop = BusStop.objects.create(place=unique_place, stop_time=timezone.now())
        self.assertIsInstance(bus_stop, BusStop)
        self.assertEqual(bus_stop.place, unique_place)

    def test_create_bus_shift_with_valid_stops(self):
        """Test that creating a BusShift with two stops is valid."""
        bus_shift = BusShift(bus=self.bus, driver=self.driver)
        bus_shift.save()

        bus_stop1 = BusStop.objects.create(place=self.place1, stop_time=self.stop_time1)
        bus_stop2 = BusStop.objects.create(place=self.place2, stop_time=self.stop_time2)
        bus_shift.stops.add(bus_stop1, bus_stop2)

        try:
            bus_shift.clean()
            bus_shift.save()
            self.assertIsNotNone(bus_shift.pk)
        except ValidationError as e:
            self.fail(f"BusShift creation failed: {str(e)}")

    def test_bus_shift_with_two_stops(self):
        """Test that a BusShift with exactly two stops passes validation."""
        bus_stop1 = BusStop.objects.create(place=self.place1, stop_time=self.stop_time1)
        bus_stop2 = BusStop.objects.create(place=self.place2, stop_time=self.stop_time2)

        bus_shift = BusShift(bus=self.bus, driver=self.driver)
        bus_shift.save()
        bus_shift.stops.add(bus_stop1, bus_stop2)

        try:
            bus_shift.clean()
        except ValidationError:
            self.fail("BusShift.clean() raised ValidationError unexpectedly with two stops.")

    def test_unique_bus_stop_constraint(self):
        """Test that creating duplicate BusStops raises an IntegrityError."""
        place = Place.objects.create(name="Unique Place", longitude=1.0, latitude=2.0)

        BusStop.objects.create(name="Stop A", place=place, stop_time=timezone.now())

        with self.assertRaises(IntegrityError):
            BusStop.objects.create(name="Stop A", place=place, stop_time=timezone.now())


class BusShiftFormTests(TestCase):

    def setUp(self):
        self.bus = Bus.objects.create(licence_plate="BUS1")
        self.driver = Driver.objects.create(user=self.create_user())
        self.place1 = Place.objects.create(name="Stop 1", longitude=0.0, latitude=0.0)
        self.place2 = Place.objects.create(name="Stop 2", longitude=0.1, latitude=0.1)
        self.stop_time1 = timezone.now()
        self.stop_time2 = self.stop_time1 + timedelta(minutes=10)
        self.start_time1 = timezone.now() + timedelta(hours=2)
        self.end_time1 = self.start_time1 + timedelta(hours=1)
        self.bus_shift1 = BusShift.objects.create(
            bus=self.bus,
            driver=self.driver,
            start_time=self.start_time1,
            end_time=self.end_time1
        )

    def create_user(self):
        """Helper method to create a user for the driver."""
        User = get_user_model()
        return User.objects.create_user(username="driver_user", password="password")

    def test_valid_form_with_two_unique_stops(self):
        """Test that a form with two unique stops is valid."""
        bus_stop1 = BusStop.objects.create(place=self.place1, stop_time=self.stop_time1)
        bus_stop2 = BusStop.objects.create(place=self.place2, stop_time=self.stop_time2)

        form_data = {
            'bus': self.bus.id,
            'driver': self.driver.id,
            'stops': [bus_stop1.id, bus_stop2.id],
        }
        form = BusShiftForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_with_one_stop(self):
        """Test that a form with one stop raises a ValidationError."""
        bus_stop1 = BusStop.objects.create(place=self.place1, stop_time=self.stop_time1)

        form_data = {
            'bus': self.bus.id,
            'driver': self.driver.id,
            'stops': [bus_stop1.id],
        }
        form = BusShiftForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertEqual(form.errors['__all__'], ["At least two bus stops are required."])

    def test_form_with_no_stops(self):
        """Test that a form with no stops raises a ValidationError."""
        form_data = {
            'bus': self.bus.id,
            'driver': self.driver.id,
            'stops': [],
        }
        form = BusShiftForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('stops', form.errors)
        self.assertEqual(form.errors['stops'], ["This field is required."])

    def test_calculate_shift_times(self):
        """Test that the shift times are calculated correctly."""
        bus_stop1 = BusStop.objects.create(place=self.place1, stop_time=self.stop_time1)
        bus_stop2 = BusStop.objects.create(place=self.place2, stop_time=self.stop_time2)

        form_data = {
            'bus': self.bus.id,
            'driver': self.driver.id,
            'stops': [bus_stop1.id, bus_stop2.id],
        }
        form = BusShiftForm(data=form_data)
        if form.is_valid():
            bus_shift = form.save()
            self.assertEqual(bus_shift.start_time, self.stop_time1)
            self.assertEqual(bus_shift.end_time, self.stop_time2)
            self.assertEqual(bus_shift.duration, self.stop_time2 - self.stop_time1)

    def test_no_overlap_with_another_shift(self):
        """Test that non-overlapping shifts do not raise a ValidationError."""
        bus_shift3 = BusShift(
            bus=self.bus,
            driver=self.driver,
            start_time=self.start_time1,
            end_time=self.end_time1
        )

        try:
            bus_shift3.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly!")
