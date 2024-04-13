from rest_framework.serializers import ModelSerializer
from ...apps.route.models import BusStop


class BusStopSerializer(ModelSerializer):
    class Meta:
        model = BusStop
        fields = ["id", "place", "transit_time"]

