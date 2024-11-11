from django.test import TestCase

from padam_django.apps.fleet.factories import BusFactory, DriverFactory
from padam_django.apps.geography.factories import PlaceFactory, BusStopFactory
from padam_django.apps.schedules.models import BusShift, BusShiftForm
from datetime import datetime

class BusShiftTestCase(TestCase):
    def setUp(self):
        self.bus = BusFactory()
        self.driver = DriverFactory()

        tmp_bus_stops = BusStopFactory.create_batch(size=5)
        self.bus_stops = sorted(tmp_bus_stops, key=lambda x: x.expected_arrival)

    def test_bus_shift_creation(self):
        bus_shift = BusShift.objects.create(
            bus=self.bus,
            driver=self.driver,
            start_time=self.bus_stops[0].expected_arrival,
            end_time=self.bus_stops[2].expected_arrival
        )
        bus_shift.bus_stops.set(self.bus_stops)

        self.assertEqual(bus_shift.bus, self.bus)
        self.assertEqual(bus_shift.driver, self.driver)
        self.assertEqual(bus_shift.start_time, self.bus_stops[0].expected_arrival)
        self.assertEqual(bus_shift.end_time, self.bus_stops[2].expected_arrival)
        self.assertEqual(bus_shift.bus_stops.count(), 5)

    def test_bus_shift_form_with_less_than_two_stops(self):
        bus_shift = BusShiftForm({
            'bus': self.bus.pk,
            'driver': self.driver.pk,
            'bus_stops': [self.bus_stops[0].pk],
        })

        self.assertFalse(bus_shift.is_valid())
        self.assertIn('__all__', bus_shift.errors)

    def test_bus_shift_form_with_two_stops(self):
        bus_shift = BusShiftForm({
            'bus': self.bus.pk,
            'driver': self.driver.pk,
            'bus_stops': [self.bus_stops[0].pk, self.bus_stops[1].pk],
        })

        self.assertTrue(bus_shift.is_valid())
        bus_shift.save()
        self.assertEqual(BusShift.objects.count(), 1)
        bus_shift = BusShift.objects.first()
        self.assertEqual(bus_shift.bus, self.bus)

    def test_bus_shift_from_with_overlapping(self):
        bus_shift1 = BusShiftForm({
            'bus': self.bus.pk,
            'driver': self.driver.pk,
            'bus_stops': [self.bus_stops[0].pk, self.bus_stops[1].pk],
        })
        self.assertTrue(bus_shift1.is_valid())
        bus_shift1.save()

        bus_shift2 = BusShiftForm({
            'bus': self.bus.pk,
            'driver': self.driver.pk,
            'bus_stops': [self.bus_stops[0].pk, self.bus_stops[2].pk],
        })

        self.assertFalse(bus_shift2.is_valid())
        self.assertIn('__all__', bus_shift2.errors)

    def test_bus_shift_from_without_overlapping(self):
        bus_shift1 = BusShiftForm({
            'bus': self.bus.pk,
            'driver': self.driver.pk,
            'bus_stops': [self.bus_stops[0].pk, self.bus_stops[1].pk],
        })
        bus_shift1.save()

        bus_shift2 = BusShiftForm({
            'bus': self.bus.pk,
            'driver': self.driver.pk,
            'bus_stops': [self.bus_stops[2].pk, self.bus_stops[4].pk],
        })

        self.assertTrue(bus_shift2.is_valid())

    def test_duration_property(self):
        bus_shift = BusShiftForm({
            'bus': self.bus.pk,
            'driver': self.driver.pk,
            'bus_stops': [self.bus_stops[0].pk, self.bus_stops[1].pk],
        })

        bus_shift.save()
        bus_shift = BusShift.objects.first()
        start_time = datetime.combine(datetime.today(), self.bus_stops[0].expected_arrival)
        end_time = datetime.combine(datetime.today(), self.bus_stops[1].expected_arrival)
        self.assertEqual(bus_shift.duration, end_time - start_time)