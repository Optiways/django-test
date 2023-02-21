from django.test import TestCase
from datetime import time
from padam_django.apps.fleet.services import get_time_diff_between


class TestDates(TestCase):
    def test_get_time_diff_between_dates_only_hours(self):
        time1 = time(hour=14, minute=30)
        time2 = time(hour=20, minute=30)
        hours, minutes = get_time_diff_between(time1, time2)
        self.assertEqual(hours, 6)
        self.assertEqual(minutes, 0)

    def test_get_time_diff_between_dates_only_minutes(self):
        time1 = time(hour=20, minute=15)
        time2 = time(hour=21, minute=00)
        hours, minutes = get_time_diff_between(time1, time2)
        self.assertEqual(hours, 0)
        self.assertEqual(minutes, 45)

    def test_get_time_diff_between_dates_only_hours_reversed_order(self):
        time1 = time(hour=14, minute=30)
        time2 = time(hour=20, minute=30)
        hours, minutes = get_time_diff_between(time2, time1)
        self.assertEqual(hours, -6)
        self.assertEqual(minutes, 0)

    def test_get_time_diff_between_dates_only_minutes_reversed_order(self):
        time1 = time(hour=20, minute=15)
        time2 = time(hour=21, minute=00)
        hours, minutes = get_time_diff_between(time2, time1)
        self.assertEqual(hours, 0)
        self.assertEqual(minutes, -45)