from django.test import TestCase
from padam_django.apps.fleet.models import BusShiftForm
from padam_django.apps.fleet.factories import BusFactory, DriverFactory
from padam_django.apps.geography.factories import BusStopFactory

class BusShiftFormTest(TestCase):

    def setUp(self):
        self.bus = BusFactory()
        self.second_bus = BusFactory()
        self.driver = DriverFactory()
        self.stop1 = BusStopFactory()
        self.stop2 = BusStopFactory()

    def test_bus_shift_form_with_valid_data(self):
        form_data = {
            'bus': self.bus.id,
            'driver': self.driver.id,
            'start': '2023-10-01T08:00:00Z',
            'end': '2023-10-01T10:00:00Z',
            'bus_stop_ids': f'{self.stop1.id},{self.stop2.id}'
        }
        form = BusShiftForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_bus_shift_form_with_less_than_two_stops(self):
        form_data = {
            'bus': self.bus.id,
            'driver': self.driver.id,
            'start': '2023-10-01T08:00:00Z',
            'end': '2023-10-01T10:00:00Z',
            'bus_stop_ids': f'{self.stop1.id}'
        }
        form = BusShiftForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('There must be at least two stops.', form.errors['bus_stop_ids'])

    def test_bus_shift_form_with_invalid_stop_ids(self):
        form_data = {
            'bus': self.bus.id,
            'driver': self.driver.id,
            'start': '2023-10-01T08:00:00Z',
            'end': '2023-10-01T10:00:00Z',
            'bus_stop_ids': '999,1000'
        }
        form = BusShiftForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('One or more bus stop IDs are invalid.', form.errors['bus_stop_ids'])

    def test_bus_shift_form_with_end_time_before_start_time(self):
        form_data = {
            'bus': self.bus.id,
            'driver': self.driver.id,
            'start': '2023-10-01T10:00:00Z',
            'end': '2023-10-01T08:00:00Z',
            'bus_stop_ids': f'{self.stop1.id},{self.stop2.id}'
        }
        form = BusShiftForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('The end time must be after the start time.', form.errors['__all__'])

    def test_bus_shift_form_with_overlapping_shifts_for_bus(self):
        # Create an initial BusShift to overlap with
        initial_form_data = {
            'bus': self.bus.id,
            'driver': self.driver.id,
            'start': '2023-10-01T08:00:00Z',
            'end': '2023-10-01T10:00:00Z',
            'bus_stop_ids': f'{self.stop1.id},{self.stop2.id}'
        }
        initial_form = BusShiftForm(data=initial_form_data)
        if initial_form.is_valid():
            initial_form.save()

        # Create a new BusShift that overlaps with the initial one
        form_data = {
            'bus': self.bus.id,
            'driver': self.driver.id,
            'start': '2023-10-01T09:00:00Z',
            'end': '2023-10-01T11:00:00Z',
            'bus_stop_ids': f'{self.stop1.id},{self.stop2.id}'
        }
        form = BusShiftForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('The bus has overlapping shifts.', form.errors['__all__'])

    def test_bus_shift_form_with_overlapping_shifts_for_driver(self):
        # Create an initial BusShift to overlap with
        initial_form_data = {
            'bus': self.bus.id,
            'driver': self.driver.id,
            'start': '2023-10-01T08:00:00Z',
            'end': '2023-10-01T10:00:00Z',
            'bus_stop_ids': f'{self.stop1.id},{self.stop2.id}'
        }
        initial_form = BusShiftForm(data=initial_form_data)
        if initial_form.is_valid():
            initial_form.save()

        # Create a new BusShift that overlaps with the initial one
        form_data = {
            'bus': self.second_bus.id,
            'driver': self.driver.id,
            'start': '2023-10-01T09:00:00Z',
            'end': '2023-10-01T11:00:00Z',
            'bus_stop_ids': f'{self.stop1.id},{self.stop2.id}'
        }
        form = BusShiftForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('The driver has overlapping shifts.', form.errors['__all__'])