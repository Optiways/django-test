from rest_framework.viewsets import ModelViewSet
from .serializer import BusStopSerializer
from ...apps.route.models import BusStop


class BusStopViewSet(ModelViewSet):
    queryset = BusStop.objects.all()
    serializer_class = BusStopSerializer
