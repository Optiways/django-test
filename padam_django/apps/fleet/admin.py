from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import BusShift, BusStop
from . import models

@admin.register(models.Bus)
class BusAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Driver)
class DriverAdmin(admin.ModelAdmin):
    pass

# Permet d'ajouter les arrêts directement dans le formulaire du trajet
class BusStopInline(admin.TabularInline):
    model = BusStop
    extra = 1  # Nombre de formulaires vides supplémentaires

@admin.register(BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    inlines = [BusStopInline]
    list_display = ('bus', 'driver', 'departure_time', 'arrival_time')

    def save_related(self, request, form, formsets, change):
        # Appelle la méthode parente pour sauvegarder les inlines
        super().save_related(request, form, formsets, change)

        # Vérification du nombre d'arrêts après la sauvegarde des inlines
        if form.instance.stops.count() < 2:
            # Ajouter une erreur de validation spécifique au formulaire
         raise ValidationError('Un trajet doit avoir au moins deux arrêts.')
