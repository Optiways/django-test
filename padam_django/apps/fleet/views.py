from django.shortcuts import render
from rest_framework import viewsets
from .models import Bus, Driver
from ...api.serializers import BusSerializer, DriverSerializer

class BusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer