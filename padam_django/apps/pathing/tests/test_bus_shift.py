import datetime
from django.utils import timezone

import pytest
from django.urls import reverse
from padam_django.apps.fleet.factories import DriverFactory, BusFactory
from padam_django.apps.pathing.factories.bus_shift_factory import BusShiftFactory
from padam_django.apps.pathing.factories.bus_stop_factory import BusStopFactory
from padam_django.apps.pathing.models import BusShift


@pytest.mark.django_db
class TestAdminBusShift:
    def test_add_bus_shift(self, authenticated_client):
        bus = BusFactory()
        driver = DriverFactory()
        bus_stop_1 = BusStopFactory()
        bus_stop_2 = BusStopFactory()
        data = {
            'bus': bus.id,
            'driver': driver.id,
            'bus_stops': [bus_stop_1.id, bus_stop_2.id],
        }
        url = reverse('admin:pathing_busshift_add')
        response = authenticated_client.post(url, data)
        assert response.status_code == 302
        assert BusShift.objects.count() == 1
        bus_shift = BusShift.objects.first()
        assert bus_shift.bus.id == bus.id

    def test_add_bus_shift_only_one_stop(self, authenticated_client):
        bus = BusFactory()
        driver = DriverFactory()
        bus_stop_1 = BusStopFactory()
        data = {
            'bus': bus.id,
            'driver': driver.id,
            'bus_stops': [bus_stop_1.id],
        }
        url = reverse('admin:pathing_busshift_add')
        response = authenticated_client.post(url, data)
        assert response.status_code == 200
        assert BusShift.objects.count() == 0
        assert "You must select at least 2 bus stops." in response.content.decode()


    def test_add_bus_shift_overlap_bus(self, authenticated_client):
        bus = BusFactory()
        driver = DriverFactory()
        now = timezone.now()
        bus_stop_1 = BusStopFactory(visit_date_time=now + datetime.timedelta(hours=1))
        bus_stop_2 = BusStopFactory(visit_date_time=now + datetime.timedelta(hours=2))
        bus_stop_3 = BusStopFactory(visit_date_time=now + datetime.timedelta(hours=3))
        bus_stop_4 = BusStopFactory(visit_date_time=now + datetime.timedelta(hours=4))
        shift = BusShiftFactory(bus=bus, bus_stops=[bus_stop_2, bus_stop_4])
        shift.bus_stops.add(bus_stop_2, bus_stop_4)
        data = {
            'bus': bus.id,
            'driver': driver.id,
            'bus_stops': [bus_stop_1.id, bus_stop_3.id],
        }
        url = reverse('admin:pathing_busshift_add')
        response = authenticated_client.post(url, data)
        assert response.status_code == 200
        assert "This bus or driver is already assigned to a shift during this time." in response.content.decode()




