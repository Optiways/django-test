import pytest
import datetime
from django.urls import reverse
from django.utils.timezone import now
from padam_django.apps.geography.factories import PlaceFactory
from padam_django.apps.pathing.models import BusStop
from django.core.exceptions import ValidationError


@pytest.mark.django_db
class TestAdminBusStop:

    def test_admin_add_bus_stop(self, authenticated_client):
        place = PlaceFactory()

        url = reverse('admin:pathing_busstop_add')
        future_datetime = now() + datetime.timedelta(days=1)
        data = {
            'visit_date_time_0': future_datetime.strftime('%Y-%m-%d'),
            'visit_date_time_1': future_datetime.strftime('%H:%M:%S'),
            'place': place.id,
        }

        response = authenticated_client.post(url, data)

        assert response.status_code == 302
        assert BusStop.objects.count() == 1
        bus_stop = BusStop.objects.first()
        assert bus_stop.place == place

    def test_admin_add_bus_stop_passed_datetime(self, authenticated_client):
        place = PlaceFactory()

        url = reverse('admin:pathing_busstop_add')
        future_datetime = now() - datetime.timedelta(days=1)
        data = {
            'visit_date_time_0': future_datetime.strftime('%Y-%m-%d'),
            'visit_date_time_1': future_datetime.strftime('%H:%M:%S'),
            'place': place.id,
        }

        response = authenticated_client.post(url, data)
        assert response.status_code == 200
        assert BusStop.objects.count() == 0
        assert "The visit date and time can&#x27;t be in the past." in response.content.decode()

@pytest.mark.django_db
class TestBusStopModel:
    def test_bus_stop_model(self):
        place = PlaceFactory()
        future_datetime = now() + datetime.timedelta(days=1)
        bus_stop = BusStop(
            visit_date_time= future_datetime,
            place= place,
        )
        bus_stop.save()
        assert BusStop.objects.count() == 1

    def test_bus_stop_model_past_date(self):
        place = PlaceFactory()
        past_datetime = now() - datetime.timedelta(days=1)
        bus_stop = BusStop(
            visit_date_time= past_datetime,
            place= place,
        )
        with pytest.raises(ValidationError, match="The visit date and time can't be in the past."):
            bus_stop.save()

        assert BusStop.objects.count() == 0