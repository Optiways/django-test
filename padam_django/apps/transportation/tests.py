from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone
from .models import BusStop, BusShift
from .forms import BusShiftForm
from .admin import BusShiftAdmin, BusStopAdmin
from ..users.models import User
from ..fleet.factories import BusFactory, DriverFactory
from ..transportation.forms import BusShiftForm
from ..geography.models import Place
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import site

class BusShiftTests(TestCase):
    def setUp(self):
        self.bus1 = BusFactory()
        self.driver1 = DriverFactory()
        self.bus2 = BusFactory()
        self.driver2 = DriverFactory()
        self.place1 = Place.objects.create(name="Place 1", longitude=0.0, latitude=0.0)
        self.place2 = Place.objects.create(name="Place 2", longitude=1.0, latitude=1.0)
        self.stop1 = BusStop.objects.create(place=self.place1, arrival_time=timezone.now())
        self.stop2 = BusStop.objects.create(place=self.place2, arrival_time=timezone.now() + timedelta(hours=1))

    def tearDown(self):
        BusStop.objects.all().delete()
        BusShift.objects.all().delete()
        Place.objects.all().delete()

    def test_1_create_bus_shift_with_less_than_two_stops(self):
        form_data = {
            'bus': self.bus1.id,
            'driver': self.driver1.id,
            'stops': [self.stop1.id]
        }
        form = BusShiftForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('stops', form.errors)
        self.assertIn('At least two stops are required', form.errors['stops'])

    def test_2_create_bus_shift_with_two_stops(self):
        form_data = {
            'bus': self.bus1.id,
            'driver': self.driver1.id,
            'stops': [self.stop1.id, self.stop2.id]
        }
        form = BusShiftForm(data=form_data)
        
        self.assertTrue(form.is_valid())
        
        bus_shift = form.save()
        self.assertEqual(bus_shift.stops.count(), 2)
        self.assertEqual(bus_shift.departure_time, self.stop1.arrival_time)
        self.assertEqual(bus_shift.arrival_time, self.stop2.arrival_time)
        self.assertAlmostEqual(bus_shift.shift_duration.total_seconds(), timedelta(hours=1).total_seconds(), delta=1)

    def test_3_bus_availability_conflict(self):
        form_data1 = {
            'bus': self.bus1.id,
            'driver': self.driver1.id,
            'stops': [self.stop1.id, self.stop2.id]
        }
        form1 = BusShiftForm(data=form_data1)
        self.assertTrue(form1.is_valid())
        bus_shift1 = form1.save()

        stop3 = BusStop.objects.create(place=self.place1, arrival_time=timezone.now() + timedelta(minutes=30))
        stop4 = BusStop.objects.create(place=self.place2, arrival_time=timezone.now() + timedelta(hours=1, minutes=30))
        
        form_data2 = {
            'bus': self.bus1.id,
            'driver': self.driver2.id,
            'stops': [stop3.id, stop4.id]
        }
        form2 = BusShiftForm(data=form_data2)
               
        self.assertFalse(form2.is_valid())
        self.assertIn('__all__', form2.errors)
        self.assertIn('The bus', form2.errors['__all__'][0])

    def test_4_driver_availability_conflict(self):
        form_data1 = {
            'bus': self.bus1.id,
            'driver': self.driver1.id,
            'stops': [self.stop1.id, self.stop2.id]
        }
        form1 = BusShiftForm(data=form_data1)
        self.assertTrue(form1.is_valid())
        bus_shift1 = form1.save()

        bus2 = BusFactory()
        stop3 = BusStop.objects.create(place=self.place1, arrival_time=timezone.now() + timedelta(minutes=30))
        stop4 = BusStop.objects.create(place=self.place2, arrival_time=timezone.now() + timedelta(hours=1, minutes=30))
        
        form_data2 = {
            'bus': bus2.id,
            'driver': self.driver1.id,
            'stops': [stop3.id, stop4.id]
        }
        form2 = BusShiftForm(data=form_data2)

        self.assertFalse(form2.is_valid())
        self.assertIn('__all__', form2.errors)
        self.assertIn('The driver', form2.errors['__all__'][0])

    def test_5_bus_shift_form_valid(self):
        form_data = {
            'bus': self.bus1.id,
            'driver': self.driver1.id,
            'stops': [self.stop1.id, self.stop2.id]
        }
        
        form = BusShiftForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        bus_shift = form.save()
        self.assertEqual(bus_shift.stops.count(), 2)
        self.assertEqual(bus_shift.departure_time, self.stop1.arrival_time)
        self.assertEqual(bus_shift.arrival_time, self.stop2.arrival_time)
        self.assertAlmostEqual(bus_shift.shift_duration.total_seconds(), timedelta(hours=1).total_seconds(), delta=1)

User = get_user_model()

class BusShiftAdminTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.bus1 = BusFactory()
        self.driver1 = DriverFactory()
        self.place1 = Place.objects.create(name="Place 1", longitude=0.0, latitude=0.0)
        self.place2 = Place.objects.create(name="Place 2", longitude=1.0, latitude=1.0)
        self.stop1 = BusStop.objects.create(place=self.place1, arrival_time=timezone.now())
        self.stop2 = BusStop.objects.create(place=self.place2, arrival_time=timezone.now() + timedelta(hours=1))
        self.admin_user = self._create_user('admin', 'admin@example.com', 'password', is_staff=True, is_superuser=True)
        self.client.login(username='admin', password='password')

    def _create_user(self, username, email, password, is_staff=False, is_superuser=False):
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
        return user

    def test_create_bus_shift_via_admin(self):
        form_data = {
            'bus': self.bus1.id,
            'driver': self.driver1.id,
            'stops': [self.stop1.id, self.stop2.id]
        }
        
        response = self.client.post('/admin/transportation/busshift/add/', form_data)
        self.assertEqual(response.status_code, 302)  # Check for a successful redirect

        # Fetch the created BusShift
        bus_shift = BusShift.objects.latest('id')
        
        # Verify that the data is correct
        self.assertEqual(bus_shift.bus, self.bus1)
        self.assertEqual(bus_shift.driver, self.driver1)
        self.assertEqual(bus_shift.stops.count(), 2)
        self.assertEqual(bus_shift.departure_time, self.stop1.arrival_time)
        self.assertEqual(bus_shift.arrival_time, self.stop2.arrival_time)
        self.assertAlmostEqual(bus_shift.shift_duration.total_seconds(), timedelta(hours=1).total_seconds(), delta=1)
        
        # Now check the admin list display values
        bus_shift_admin = BusShiftAdmin(BusShift, site)
        self.assertEqual(bus_shift_admin.departure_time_display(bus_shift), bus_shift.departure_time)
        self.assertEqual(bus_shift_admin.arrival_time_display(bus_shift), bus_shift.arrival_time)
        self.assertEqual(bus_shift_admin.shift_duration_display(bus_shift), '1h 0m')

    def test_bus_stop_admin_display(self):
        # Create a BusStop instance
        bus_stop = BusStop.objects.create(
            place=self.place1,
            arrival_time=timezone.now()
        )

        # Check if the admin display is correct
        bus_stop_admin = BusStopAdmin(BusStop, site)
        list_display = bus_stop_admin.get_list_display(None)
        self.assertIn('place', list_display)
        self.assertIn('arrival_time', list_display)