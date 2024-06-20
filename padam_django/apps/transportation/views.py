from django.shortcuts import render
from rest_framework import viewsets
from .models import BusShift, BusStop
from ...api.serializers import BusStopSerializer, BusShiftSerializer, BusSerializer, DriverSerializer


class BusStopViewSet(viewsets.ModelViewSet):
    queryset = BusStop.objects.all()
    serializer_class = BusStopSerializer

class BusShiftViewSet(viewsets.ModelViewSet):
    queryset = BusShift.objects.all()
    serializer_class = BusShiftSerializer