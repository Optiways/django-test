from rest_framework.serializers import ModelSerializer
from ...apps.route.models import BusShift


class BusShiftSerializer(ModelSerializer):
    class Meta:
        model = BusShift
        fields = ["id", "bus", "driver", "stops", "departure_time", "arrival_time", "shift_duration"]

