import datetime

from django.core import management
from django.core.exceptions import ValidationError
from django.test import TestCase

from padam_django.apps.fleet.models import Bus, Driver
from padam_django.apps.geography.models import Place
from padam_django.apps.travel.models import BusShift, StartBusStop, EndBusStop
from padam_django.apps.users.models import User


class TravelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        management.call_command("create_data")

    def test_bus_stop_validation(self):
        user = User.objects.filter(driver__isnull=True).first()
        user_driver = User.objects.filter(driver__isnull=False).first()
        place = Place.objects.first()
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        wrong_ts_requested = now - datetime.timedelta(days=1)

        # Testing ts_requested validator
        with self.assertRaises(ValidationError):
            start_bus_stop = StartBusStop(
                user=user, place=place, ts_requested=wrong_ts_requested
            )
            start_bus_stop.full_clean()

        ts_requested = now + datetime.timedelta(days=1)
        # A driver can't be a passenger
        with self.assertRaises(ValidationError):
            start_bus_stop = StartBusStop(
                user=user_driver, place=place, ts_requested=wrong_ts_requested
            )
            start_bus_stop.full_clean()

        start_bus_stop = StartBusStop.objects.create(
            user=user, place=place, ts_requested=ts_requested
        )
        start_bus_stop.full_clean()

        end_ts_requested = ts_requested + datetime.timedelta(minutes=30)
        with self.assertRaises(ValidationError):
            end_bus_stop = EndBusStop(
                start=start_bus_stop, place=place, ts_requested=end_ts_requested
            )
            end_bus_stop.full_clean()

        end_place = Place.objects.exclude(pk=place.pk).first()
        with self.assertRaises(ValidationError):
            end_bus_stop = EndBusStop(
                start=start_bus_stop, place=end_place, ts_requested=ts_requested
            )
            end_bus_stop.full_clean()

        end_bus_stop = EndBusStop.objects.create(
            start=start_bus_stop, place=end_place, ts_requested=end_ts_requested
        )
        end_bus_stop.full_clean()

        # Itinerary can't overlap
        between_ts_requested = ts_requested + (end_ts_requested - ts_requested) / 2
        with self.assertRaises(ValidationError):
            start_bus_stop = StartBusStop(
                user=user, place=place, ts_requested=between_ts_requested
            )
            start_bus_stop.full_clean()

        # The overlap checks only for the current user
        user_2 = User.objects.filter(driver__isnull=True).exclude(pk=user.pk).first()
        start_bus_stop = StartBusStop.objects.create(
            user=user_2, place=place, ts_requested=between_ts_requested
        )
        start_bus_stop.full_clean()

        ts_requested_2 = ts_requested - datetime.timedelta(minutes=30)
        start_bus_stop_2 = StartBusStop.objects.create(
            user=user, place=place, ts_requested=ts_requested_2
        )
        start_bus_stop_2.full_clean()

        # Itinerary can't overlap
        with self.assertRaises(ValidationError):
            end_bus_stop = EndBusStop(
                start=start_bus_stop_2, place=place, ts_requested=between_ts_requested
            )
            end_bus_stop.full_clean()

    def test_bus_shift_validation(self):
        passenger = User.objects.filter(driver__isnull=True).first()
        passenger_2 = (
            User.objects.exclude(pk=passenger.pk).filter(driver__isnull=True).first()
        )
        place = Place.objects.first()
        place_2 = Place.objects.exclude(pk=place.pk).first()
        now = datetime.datetime.now(tz=datetime.timezone.utc)

        ts_requested = now + datetime.timedelta(days=1)
        start_bus_stop = StartBusStop.objects.create(
            user=passenger, place=place, ts_requested=ts_requested
        )
        end_ts_requested = ts_requested + datetime.timedelta(minutes=30)
        end_bus_stop = EndBusStop.objects.create(
            start=start_bus_stop, place=place_2, ts_requested=end_ts_requested
        )

        driver = Driver.objects.first()
        bus = Bus.objects.first()
        bus_shift = BusShift.objects.create(driver=driver, bus=bus)
        end_bus_stop.shift = bus_shift
        end_bus_stop.save(update_fields=["shift"])
        self.assertEquals(bus_shift.shift_start, ts_requested)
        self.assertEquals(bus_shift.shift_end, end_ts_requested)
        self.assertEquals(bus_shift.shift_duration, end_ts_requested - ts_requested)

        ts_requested_2 = ts_requested - datetime.timedelta(minutes=30)
        start_bus_stop_2 = StartBusStop.objects.create(
            user=passenger_2, place=place, ts_requested=ts_requested_2
        )
        end_ts_requested_2 = end_ts_requested + datetime.timedelta(minutes=30)
        end_bus_stop_2 = EndBusStop.objects.create(
            start=start_bus_stop_2, place=place_2, ts_requested=end_ts_requested_2
        )
        driver_2 = Driver.objects.exclude(pk=driver.pk).first()
        bus_2 = Bus.objects.exclude(pk=bus.pk).first()

        stops = EndBusStop.objects.filter(pk=end_bus_stop_2.pk)
        # The bus is already used by the first shift
        with self.assertRaises(ValidationError):
            bus_shift_2 = BusShift(driver=driver_2, bus=bus)
            bus_shift_2.clean_or_validate(stops)

        # The driver is already on the first shift
        with self.assertRaises(ValidationError):
            bus_shift_2 = BusShift(driver=driver, bus=bus_2)
            bus_shift_2.clean_or_validate(stops)

        bus_shift_2 = BusShift(driver=driver_2, bus=bus_2)
        bus_shift_2.clean_or_validate(stops)

        end_bus_stop_2.shift = bus_shift
        end_bus_stop_2.save(update_fields=["shift"])
        self.assertEquals(bus_shift.shift_start, ts_requested_2)
        self.assertEquals(bus_shift.shift_end, end_ts_requested_2)
        self.assertEquals(bus_shift.shift_duration, end_ts_requested_2 - ts_requested_2)
