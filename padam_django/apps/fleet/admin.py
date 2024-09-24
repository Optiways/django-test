from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ValidationError as FormValidationError
from .models import BusShift, BusStop, Bus, Driver

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    """
    Interface d'administration pour le modèle Bus.
    """
    list_display = ('licence_plate',)
    search_fields = ('licence_plate',)
    ordering = ('licence_plate',)

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    """
    Interface d'administration pour le modèle Driver.
    """
    list_display = ('user',)
    search_fields = ('user__username',)
    ordering = ('user__username',)

class BusStopInline(admin.TabularInline):
    """
    Inline admin pour le modèle BusStop.
    Permet d'ajouter des arrêts directement dans le formulaire du trajet.
    """
    model = BusStop
    extra = 1  # Nombre de formulaires vides supplémentaires
    fields = ('order', 'place', 'passing_time')
    ordering = ('order',)

@admin.register(BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    """
    Interface d'administration pour le modèle BusShift.
    Gère la création et la modification des trajets et de leurs arrêts associés.
    """
    inlines = [BusStopInline]
    list_display = ('bus', 'driver', 'departure_time', 'arrival_time')
    fields = ('bus', 'driver', 'departure_time', 'arrival_time')
    search_fields = ('bus__licence_plate', 'driver__user__username')
    ordering = ('departure_time',)

    def save_model(self, request, obj, form, change):
        """
        Sauvegarde le BusShift.
        Ne fait pas de validation complète ici car les BusStops ne sont pas encore sauvegardés.
        """
        obj.save()

    def save_related(self, request, form, formsets, change):
        """
        Sauvegarde les objets liés (BusStops) et met à jour les heures du BusShift.
        Effectue ensuite une validation complète du BusShift.
        """
        # Sauvegarde des BusStops associés
        super().save_related(request, form, formsets, change)
        obj = form.instance

        # Mettre à jour les heures du BusShift en fonction des BusStops
       # obj.update_times_from_stops()

        # Vérifier qu'il y a au moins deux BusStops
        if obj.stops.count() < 2:
            form.add_error(None, 'Un trajet doit avoir au moins deux arrêts.')
            raise FormValidationError('Un trajet doit avoir au moins deux arrêts.')

        # Effectuer les validations après que les heures aient été mises à jour
        try:
            obj.full_clean()
            obj.save()
        except ValidationError as e:
            self._add_errors_to_form(form, e)
            raise FormValidationError(e)

    def _add_errors_to_form(self, form, error):
        """
        Ajoute les erreurs de ValidationError au formulaire pour affichage dans l'admin.
        """
        if hasattr(error, 'error_dict'):
            # Erreurs spécifiques aux champs
            for field, field_errors in error.error_dict.items():
                for field_error in field_errors:
                    form.add_error(field, field_error)
        else:
            # Erreurs générales
            for err in error.error_list:
                form.add_error(None, err)
