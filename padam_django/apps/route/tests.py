from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase

from ..fleet.factories import BusFactory, DriverFactory
from ..route.forms import BusShiftForm
from .factories import BusShiftFactory, BusStopFactory


class BusShiftModelTestCase(TestCase):

    def setUp(self) -> None:
        self.bus = BusFactory()
        self.driver = DriverFactory()

    def test_check_bus_availability_raises_validation_error(self):
        """
        Test if the '_check_bus_availability' method raises a ValidationError
        when trying to create a new BusShift instance with the same bus and time range.
        """
        stops = BusStopFactory.create_batch(2)
        existing_shift = BusShiftFactory(bus=self.bus, driver=self.driver)
        existing_shift.stops.set(stops)
        existing_shift.save()

        # try to create a new BusShift instance with the same bus and time range
        form = BusShiftForm(data={
            'bus': existing_shift.bus.pk,
            'driver': existing_shift.driver.pk,
         })
        with self.assertRaises(ValidationError):
            form._check_bus_availability(existing_shift.departure_time, existing_shift.arrival_time, existing_shift.bus)

    def test_overlapping_shifts_raise_validation_error(self):
        """
        Test if overlapping bus shifts raise a ValidationError when validating the form.
        """
        # Create a bus shift with two bus stops
        stops1 = BusStopFactory.create_batch(2)
        existing_shift1 = BusShiftFactory(bus=self.bus, driver=self.driver)
        existing_shift1.stops.set(stops1)
        existing_shift1.save()

        # Create a bus shift with two bus stops, overlapping the first shift
        departure_time_overlap = existing_shift1.departure_time + timedelta(minutes=30)
        arrival_time_overlap = existing_shift1.arrival_time + timedelta(minutes=30)
        stops2 = [
            BusStopFactory(transit_time=departure_time_overlap),
            BusStopFactory(transit_time=arrival_time_overlap)
        ]
        form = BusShiftForm(data={
            'bus': self.bus.pk,
            'driver': self.driver.pk,
            'stops': [stop.pk for stop in stops2],
        })

        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertIn('This bus is already booked for a shift', form.errors['__all__'])

    def test_overlapping_drivers_raise_validation_error(self):
        """
        Test if overlapping driver shifts raise a ValidationError when validating the form.
        """
        # Create a bus shift with two bus stops
        stops1 = BusStopFactory.create_batch(2)
        existing_shift1 = BusShiftFactory(bus=self.bus, driver=self.driver)
        existing_shift1.stops.set(stops1)
        existing_shift1.save()

        bus1 = BusFactory()
        # Create a bus shift with two bus stops, overlapping the first shift
        departure_time_overlap = existing_shift1.departure_time + timedelta(minutes=30)
        arrival_time_overlap = existing_shift1.arrival_time + timedelta(minutes=30)
        stops2 = [
            BusStopFactory(transit_time=departure_time_overlap),
            BusStopFactory(transit_time=arrival_time_overlap)
        ]
        form = BusShiftForm(data={
            'bus': bus1.pk,
            'driver': self.driver.pk,
            'stops': [stop.pk for stop in stops2],
        })

        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertIn('This driver is already on a shift', form.errors['__all__'])

    def test_one_stop_raise_validation_error(self):
        """
        Test if having only one bus stop in a BusShift raises a ValidationError when validating the form.
        """
        # Create a bus shift with only one bus stop
        stop = BusStopFactory.create_batch(1)
        existing_shift1 = BusShiftFactory(bus=self.bus, driver=self.driver)
        existing_shift1.stops.set(stop)
        existing_shift1.save()

        form = BusShiftForm(data={
            'bus': self.bus.pk,
            'driver': self.driver.pk,
            'stops': [stop[0].pk],
        })

        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)
        self.assertIn('At least two stops are required', form.errors['__all__'])

    def test_no_error_when_shifts_do_not_overlap(self):
        """
        Test if no validation error is raised when bus shifts do not overlap.
        """
        # Create a bus shift with only two stops
        stops = BusStopFactory.create_batch(2)
        existing_shift = BusShiftFactory(bus=self.bus, driver=self.driver)
        existing_shift.stops.set(stops)
        existing_shift.save()
        departure_time_new = existing_shift.arrival_time + timedelta(minutes=10)
        arrival_time_new = existing_shift.arrival_time + timedelta(hours=2)
        new_stops = [
            BusStopFactory(transit_time=departure_time_new),
            BusStopFactory(transit_time=arrival_time_new)
        ]
        form = BusShiftForm(
            data={
                'bus': self.bus.pk,
                'driver': self.driver.pk,
                'stops': [stop.pk for stop in new_stops]
            },
        )
        self.assertTrue(form.is_valid())
