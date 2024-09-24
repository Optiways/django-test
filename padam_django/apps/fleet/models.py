from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Min, Max
from padam_django.apps.geography.models import Place  # Import du modèle Place depuis l'application geography

class Driver(models.Model):
    """
    Modèle représentant un chauffeur de bus, lié à un utilisateur.
    """
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        related_name='driver',
        help_text='Compte utilisateur associé au chauffeur.'
    )

    def __str__(self):
        return f"Chauffeur: {self.user.username} (ID: {self.pk})"

class Bus(models.Model):
    """
    Modèle représentant un bus, identifié par sa plaque d'immatriculation.
    """
    licence_plate = models.CharField(
        "Plaque d'immatriculation",
        max_length=10,
        unique=True,
        help_text='Plaque d\'immatriculation unique du bus.'
    )

    class Meta:
        verbose_name_plural = "Bus"

    def __str__(self):
        return f"Bus: {self.licence_plate} (ID: {self.pk})"

class BusShift(models.Model):
    """
    Modèle représentant un trajet de bus (service), associé à un bus et un chauffeur.
    Les heures de départ et d'arrivée sont déterminées en fonction des arrêts associés.
    """
    bus = models.ForeignKey(
        'Bus',
        on_delete=models.CASCADE,
        help_text='Bus affecté à ce trajet.'
    )
    driver = models.ForeignKey(
        'Driver',
        on_delete=models.CASCADE,
        help_text='Chauffeur affecté à ce trajet.'
    )
    departure_time = models.DateTimeField(
        help_text='Heure de départ du trajet.'
    )
    arrival_time = models.DateTimeField(
        help_text='Heure d\'arrivée du trajet.'
    )

    def clean(self):
        """
        Valide l'instance de BusShift.
        - Vérifie que les heures de départ et d'arrivée sont définies.
        - Vérifie que l'heure d'arrivée est postérieure à l'heure de départ.
        - Vérifie qu'il n'y a pas de chevauchement avec d'autres trajets pour le même bus ou chauffeur.
        """
        # Vérifier que les heures de départ et d'arrivée sont définies
        if not self.departure_time or not self.arrival_time:
            raise ValidationError('Les heures de départ et d\'arrivée doivent être définies.')
        
        # Vérifier que l'heure d'arrivée est après l'heure de départ
        if self.arrival_time <= self.departure_time:
            raise ValidationError('L\'heure d\'arrivée doit être après l\'heure de départ.')

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


    # Ne fonctionne pas
    def update_times_from_stops(self):
        """
        Met à jour departure_time et arrival_time en fonction des BusStops associés.
        Cette méthode doit être appelée après la sauvegarde des BusStops.
        """
        stops = self.stops.order_by('order')
        if stops.exists():
            self.departure_time = stops.first().passing_time
            self.arrival_time = stops.last().passing_time
        else:
            self.departure_time = None
            self.arrival_time = None

    def __str__(self):
        return f"Trajet {self.pk} - Bus {self.bus.licence_plate} - Chauffeur {self.driver.user.username}"

class BusStop(models.Model):
    """
    Modèle représentant un arrêt de bus dans un trajet.
    Chaque BusStop est associé à un BusShift.
    """
    bus_shift = models.ForeignKey(
        'BusShift',
        on_delete=models.CASCADE,
        related_name='stops',
        help_text='Trajet auquel cet arrêt est associé.'
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        help_text='Lieu de l\'arrêt.'
    )
    passing_time = models.DateTimeField(
        help_text='Heure de passage à l\'arrêt.'
    )
    order = models.PositiveIntegerField(
        help_text='Ordre de l\'arrêt dans le trajet.'
    )

    class Meta:
        ordering = ['order']  # Les arrêts seront triés par ordre
        unique_together = ('bus_shift', 'order')  # Un ordre unique par trajet
        verbose_name = 'Arrêt de bus'
        verbose_name_plural = 'Arrêts de bus'

    def clean(self):
        """
        Valide l'instance de BusStop.
        - Vérifie que l'ordre est positif.
        - Vérifie que passing_time est après le passing_time de l'arrêt précédent.
        """
        # Vérifier que l'ordre est positif
        if self.order < 1:
            raise ValidationError('L\'ordre doit être un entier positif.')

        # Vérifier que passing_time est cohérent avec l'arrêt précédent
        previous_stop = self.bus_shift.stops.filter(order__lt=self.order).order_by('-order').first()
        if previous_stop and self.passing_time <= previous_stop.passing_time:
            raise ValidationError('L\'heure de passage doit être après celle de l\'arrêt précédent.')

    def __str__(self):
        return f"Arrêt {self.order} à {self.place.name} pour le trajet {self.bus_shift.pk}"
