from rest_framework.viewsets import ModelViewSet
from .serializer import BusShiftSerializer
from ...apps.route.models import BusShift


class BusShiftViewSet(ModelViewSet):
    queryset = BusShift.objects.all()
    serializer_class = BusShiftSerializer
