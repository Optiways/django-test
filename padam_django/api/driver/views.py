from rest_framework.viewsets import ModelViewSet
from .serializer import DriverSerializer
from ...apps.fleet.models import Driver


class DriverViewSet(ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
