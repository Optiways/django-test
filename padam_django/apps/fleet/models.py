from django.db import models

import datetime
import pytz


class Driver(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='driver')

    def is_busy(self, start_ride, end_ride) -> bool:
        """Define if the driver is busy at the time requested."""
        # start_ride = '2022/06/17 04:58' #exemple
        # end_ride = '2022/06/17 10:27' #exemple
        d_shifts = Driver.objects.get(id=self.pk).busshift_set.all() #the driver rides
        start_ride = datetime.datetime.strptime(start_ride, '%Y/%m/%d %H:%M').replace(tzinfo=pytz.UTC) #check how to import django timezone
        end_ride = datetime.datetime.strptime(end_ride, '%Y/%m/%d %H:%M').replace(tzinfo=pytz.UTC) #check how to import django timezone
        filter_params = dict(ride_arr_time__gte=start_ride, ride_dep_time__lte=end_ride)
        return d_shifts.filter(**filter_params, driver__user__username='merleoceane').exists()

        
    def __str__(self):
        return f"Driver: {self.user.username} (id: {self.pk})"


class Bus(models.Model):
    licence_plate = models.CharField("Name of the bus", max_length=10)

    class Meta:
        verbose_name_plural = "Buses"

    def __str__(self):
        return f"Bus: {self.licence_plate} (id: {self.pk})"
