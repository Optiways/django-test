from django.db import models


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
    

class BusShift(models.Model):
    name = models.CharField('Name of the bus shift', max_length=100)
    bus = models.OneToOneField(Bus, on_delete=models.CASCADE)
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE)

    def __str__(self):
        return f"BusShift: {self.name} (id: {self.pk})"
    
    def clean(self):
        print(self)


class BusStop(models.Model):
    name = models.CharField('Name of the bus stop', max_length=100)
    time = models.DateTimeField()
    place = models.OneToOneField('geography.Place', on_delete=models.CASCADE)
    bus_shift = models.ForeignKey(BusShift, on_delete=models.CASCADE)

    def __str__(self):
        return f"BusStop: {self.name} (id: {self.pk})"
    
