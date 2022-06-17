from django.db import models
from django.db.models import Max, Min


class BusShift(models.Model):
    bus = models.ForeignKey('fleet.Bus', null=True, on_delete=models.CASCADE)
    driver = models.ForeignKey('fleet.Driver', null=True, on_delete=models.CASCADE)
    ride_arr_time = models.DateTimeField('ride arrival time', null=True)
    ride_dep_time = models.DateTimeField('ride departure time', null=True)
    
    def arr_time(self):
        b = BusShift.objects.get(id=self.pk)
        arr_time = b.busstop_set.aggregate(Max('time'))['time__max']
        # it would be better to stock the info in the db only once instead of 
        # do it every time (maybe using signal?)
        b.ride_arr_time = b.busstop_set.aggregate(Max('time'))['time__max']
        b.save()
        return arr_time

    def dep_time(self):
        b = BusShift.objects.get(id=self.pk)
        dep_time = b.busstop_set.aggregate(Min('time'))['time__min']
        # it would be better to stock the info in the db only once instead of 
        # do it every time (maybe using signal?)
        b.ride_dep_time = b.busstop_set.aggregate(Min('time'))['time__min']
        b.save()
        return dep_time
    
    def __str__(self):
        return f"Shift: { self.ride_dep_time.strftime('%d/%m/%y %H:%M') } - { self.ride_arr_time.strftime('%d/%m/%y %H:%M') } (id: {self.pk})"

class BusStop(models.Model):
    place = models.ForeignKey('geography.Place', null=True, on_delete=models.CASCADE)
    time = models.DateTimeField('arrival time', null=True)
    busshift = models.ForeignKey(BusShift, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Stop: {self.time} - {self.place.name} (id: {self.pk})"

