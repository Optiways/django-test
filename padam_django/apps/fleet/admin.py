from django.contrib import admin
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

    # Appele la méthode clean lors de la sauvegarde dans l'admin
    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)