from rest_framework.viewsets import ModelViewSet
from .serializer import BusSerializer
from ...apps.fleet.models import Bus


class BusViewSet(ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
