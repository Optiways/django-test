from rest_framework.serializers import ModelSerializer
from ...apps.fleet.models import Driver


class DriverSerializer(ModelSerializer):
    class Meta:
        model = Driver
        fields = ["id", "user"]

