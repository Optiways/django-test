from django.db import models
from django.core.exceptions import ValidationError
from padam_django.apps.geography.models import Place 

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
    bus = models.ForeignKey('Bus', on_delete=models.CASCADE)
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    def clean(self):
        # Vérifier que l'heure d'arrivée est après l'heure de départ
        if self.arrival_time <= self.departure_time:
            raise ValidationError('L\'heure d\'arrivée doit être après l\'heure de départ.')
        
         # Vérification des arrêts associés
        if self.pk and self.stops.count() < 2:  # Vérification que le trajet existe et a moins de deux arrêts
            raise ValidationError('Un trajet doit avoir au moins deux arrêts.')

        # Vérifier que le bus n'est pas déjà assigné à un autre trajet qui se chevauche
        overlapping_shifts_bus = BusShift.objects.filter(
            bus=self.bus,
            departure_time__lt=self.arrival_time,
            arrival_time__gt=self.departure_time
        ).exclude(pk=self.pk)
        if overlapping_shifts_bus.exists():
            raise ValidationError('Ce bus est déjà assigné à un autre trajet pendant cette période.')

        # Vérifier que le chauffeur n'est pas déjà assigné à un autre trajet qui se chevauche
        overlapping_shifts_driver = BusShift.objects.filter(
            driver=self.driver,
            departure_time__lt=self.arrival_time,
            arrival_time__gt=self.departure_time
        ).exclude(pk=self.pk)
        if overlapping_shifts_driver.exists():
            raise ValidationError('Ce chauffeur est déjà assigné à un autre trajet pendant cette période.')
        
    def __str__(self):
        return f"Trajet {self.pk} - Bus {self.bus.licence_plate} - Chauffeur {self.driver.user.username}"
    

class BusStop(models.Model):
    bus_shift = models.ForeignKey('BusShift', on_delete=models.CASCADE, related_name='stops')
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    passing_time = models.DateTimeField()
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']  # Les arrêts seront triés par ordre
        unique_together = ('bus_shift', 'order')  # Un ordre unique par trajet

    def __str__(self):
        return f"Arrêt {self.order} - {self.place.name} pour le trajet {self.bus_shift.pk}"
    

