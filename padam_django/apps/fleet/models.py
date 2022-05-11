from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from ..geography.models import Place

class Driver(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='driver')

    def __str__(self):
        return f"Driver: {self.user.username} (id: {self.pk})"


class Bus(models.Model):
    licence_plate = models.CharField("Name of the bus", max_length=10)

    class Meta:
        verbose_name_plural = "Buses"

    def __str__(self):
        return f"Bus: {self.licence_plate} (id: {self.pk})"


class BusStop(models.Model):
    schedule = models.DateTimeField(auto_now=False)
    place    = models.ForeignKey(Place, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Bus Stop"
        verbose_name_plural = "Bus Stops"
        ordering = ('schedule',)

    def __str__(self):
        return f"Bus stop for place : {self.place.name} "

class BusShift(models.Model):
    
    start_shift = models.DateTimeField(auto_now= False, blank= True, null = True)
    end_shift   = models.DateTimeField(auto_now= False, blank= True, null = True)
    driver      = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True)
    bus         = models.ForeignKey(Bus, on_delete=models.CASCADE, null=True)
    bus_stops   = models.ManyToManyField(BusStop)

    def __init__(self, *args, **kwargs):
        super(BusShift, self).__init__(*args, **kwargs)
        self.old_start = self.start_shift
        self.old_end = self.end_shift

    def __str__(self):
        return f"BusShift with Bus  {self.bus.licence_plate} and Driver {self.driver.user.first_name} {self.driver.user.last_name}"

    # method that return the duration of the shift
    def get_shift_duration(self):

        difference = self.end_shift - self.start_shift
        duration_in_s = difference.total_seconds()
        days    = divmod(duration_in_s, 86400)        
        hours   = divmod(days[1], 3600)               
        minutes = divmod(hours[1], 60)                
        seconds = divmod(minutes[1], 1)               

        return "The shift will last: %d days, %d hours, %d minutes and %d seconds" % (days[0], hours[0], minutes[0], seconds[0])

    '''
        Overwrite the save method to prevent busshift to have a bus or a driver allready attributed
    '''
    def save(self, *args, **kwargs):
        try:
            overlap_start_bus = BusShift.objects.filter(Q(bus = self.bus) & Q(start_shift__gte = self.start_shift , start_shift__lte = self.end_shift)).count()
            overlap_end_bus = BusShift.objects.filter( Q(bus = self.bus) & Q(end_shift__gte = self.start_shift , start_shift__lte = self.end_shift)).count()
            
            overlap_start_driver = BusShift.objects.filter(Q(driver = self.driver) & Q(start_shift__gte = self.start_shift , start_shift__lte = self.end_shift)).count()
            overlap_end_driver = BusShift.objects.filter( Q(driver = self.driver) & Q(end_shift__gte = self.start_shift , start_shift__lte = self.end_shift)).count()

            if (overlap_start_bus > 0 or overlap_end_bus > 0) or (overlap_start_driver > 0 or overlap_end_driver > 0) :
                raise ValidationError(
                    f'A driver or a bus can\'t be asigned to two shift with the sames schedules'
                )
            else:
                super(BusShift, self).save(*args, **kwargs)
        except:
             super(BusShift, self).save(*args, **kwargs)
    
 
