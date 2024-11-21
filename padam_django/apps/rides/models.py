from django.db import models
from django.db.models import Max, Min
from padam_django.apps.fleet.models import Driver

class BusShift(models.Model):
    bus = models.ForeignKey('fleet.Bus', null=True, on_delete=models.CASCADE)
    driver = models.ForeignKey('fleet.Driver', null=True, on_delete=models.CASCADE)
    ride_arr_time = models.DateTimeField('ride arrival time', null=True)
    ride_dep_time = models.DateTimeField('ride departure time', null=True)
    
    @property
    def arr_time(self):
        b = BusShift.objects.get(id=self.pk)
        arr_time = b.busstop_set.aggregate(Max('time'))['time__max']
        # it would be better to stock the info in the db only once instead of 
        # do it every time (maybe using signal?)
        b.ride_arr_time = b.busstop_set.aggregate(Max('time'))['time__max']
        b.save()
        return arr_time

    @property
    def dep_time(self):
        b = BusShift.objects.get(id=self.pk)
        dep_time = b.busstop_set.aggregate(Min('time'))['time__min']
        # it would be better to stock the info in the db only once instead of 
        # do it every time (maybe using signal?)
        b.ride_dep_time = b.busstop_set.aggregate(Min('time'))['time__min']
        b.save()
        return dep_time
    
    @property
    def available_drivers(self):
        all_rides = BusShift.objects.all()
        start_ride = self.ride_dep_time
        end_ride = self.ride_arr_time
        filter_params = dict(ride_arr_time__gte=start_ride, ride_dep_time__lte=end_ride)
        busy_drivers = all_rides.filter(**filter_params).values_list('driver__user__username')
        filters = dict(user__username__in = list(busy_drivers[0]))
        available_drivers = Driver.objects.all().exclude(**filters)
        return available_drivers
    
    def __str__(self):
        return f"Shift: { self.dep_time.strftime('%d/%m/%y %H:%M') } - { self.arr_time.strftime('%d/%m/%y %H:%M') } (id: {self.pk})"

class BusStop(models.Model):
    place = models.ForeignKey('geography.Place', null=True, on_delete=models.CASCADE)
    time = models.DateTimeField('arrival time', null=True)
    busshift = models.ForeignKey(BusShift, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Stop: {self.time} - {self.place.name} (id: {self.pk})"

