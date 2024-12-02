from rest_framework import serializers
from ..apps.transportation.models import BusStop, BusShift
from ..apps.fleet.models import Bus, Driver
from ..apps.geography.models import Place
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    is_driver = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_driver']

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'

class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Driver
        fields = ['id', 'user']

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'

class BusStopSerializer(serializers.ModelSerializer):
    place = PlaceSerializer(read_only=True)
    class Meta:
        model = BusStop
        fields = '__all__'

class BusShiftSerializer(serializers.ModelSerializer):
    stops = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=BusStop.objects.all()
    )
    departure_time = serializers.SerializerMethodField()
    arrival_time = serializers.SerializerMethodField()
    shift_duration = serializers.SerializerMethodField()

    class Meta:
        model = BusShift
        fields = ['id', 'bus', 'driver', 'stops', 'departure_time', 'arrival_time', 'shift_duration']

    def get_departure_time(self, obj):
        return obj.departure_time

    def get_arrival_time(self, obj):
        return obj.arrival_time

    def get_shift_duration(self, obj):
        duration = obj.shift_duration
        if duration:
            return duration.total_seconds() / 60  # minute
        return 0

    def validate_stops(self, stops):
        if len(stops) < 2:
            raise serializers.ValidationError("At least two stops are required.")
        return stops
    
    def validate(self, data):
        bus = data.get('bus')
        stops = data.get('stops', [])
        driver = data.get('driver')

        if stops and len(stops) >= 2:
            stops_instances = BusStop.objects.filter(id__in=[s.id for s in stops])
            departure_time = stops_instances.order_by('arrival_time').first().arrival_time
            arrival_time = stops_instances.order_by('arrival_time').last().arrival_time

            if self._has_time_conflict(BusShift.objects.filter(bus=bus), departure_time, arrival_time):
                raise serializers.ValidationError({"bus": "The bus is already booked during this period"})
            
            if self._has_time_conflict(BusShift.objects.filter(driver=driver), departure_time, arrival_time):
                raise serializers.ValidationError({"driver": "The driver is already assigned to another shift during this period"})
        
        return data
    
    def _has_time_conflict(self, shifts, start, end):
        for shift in shifts:
            if shift.departure_time <= end and shift.arrival_time >= start:
                return True
        return False
