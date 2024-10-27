import datetime

from django.core import management
from django.core.exceptions import ValidationError
from django.test import TestCase

from padam_django.apps.geography.models import Place
from padam_django.apps.travel.models import StartBusStop, EndBusStop
from padam_django.apps.users.models import User


class TravelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        management.call_command("create_data")

    def test_bus_stop_validation(self):
        user = User.objects.first()
        place = Place.objects.first()
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        wrong_ts_requested = now - datetime.timedelta(days=1)

        # Testing ts_requested validator
        with self.assertRaises(ValidationError):
            start_bus_stop = StartBusStop.objects.create(
                user=user, place=place, ts_requested=wrong_ts_requested
            )
            start_bus_stop.full_clean()
        start_bus_stop.delete()

        ts_requested = now + datetime.timedelta(days=1)
        start_bus_stop = StartBusStop.objects.create(
            user=user, place=place, ts_requested=ts_requested
        )
        start_bus_stop.full_clean()

        end_ts_requested = ts_requested + datetime.timedelta(minutes=30)
        with self.assertRaises(ValidationError):
            end_bus_stop = EndBusStop.objects.create(
                start=start_bus_stop, place=place, ts_requested=end_ts_requested
            )
            end_bus_stop.full_clean()
        end_bus_stop.delete()

        end_place = Place.objects.exclude(pk=place.pk).first()
        with self.assertRaises(ValidationError):
            end_bus_stop = EndBusStop.objects.create(
                start=start_bus_stop, place=end_place, ts_requested=ts_requested
            )
            end_bus_stop.full_clean()
        end_bus_stop.delete()

        end_bus_stop = EndBusStop.objects.create(
            start=start_bus_stop, place=end_place, ts_requested=end_ts_requested
        )
        end_bus_stop.full_clean()
