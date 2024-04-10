from rest_framework.serializers import ModelSerializer
from ...apps.fleet.models import Bus


class BusSerializer(ModelSerializer):
    class Meta:
        model = Bus
        fields = ["id", "licence_plate"]

