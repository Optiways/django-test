# System import
import uuid

# Django import.
from django import forms

# App import.
from . import models
from .validators import is_time_slot_valid
from .utils import update_fields_instance

class BusShiftForm(forms.ModelForm):
    """ Form that allow to modify and create BusShift instance

    Raises:
        forms.ValidationError: _description_
    """
    class Meta:
        model = models.BusShift
        exclude = ['']
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check if BusShift have BusStops

    def clean(self):
        # Get form input
        departure = self.cleaned_data.get('departure')
        arrival = self.cleaned_data.get('arrival')
        bus = self.cleaned_data.get('bus')
        driver = self.cleaned_data.get('driver')

        # Verify bus shift validity
        is_time_slot_valid(
            driver=driver,
            bus=bus,
            new_departure=departure, 
            new_arrival=arrival
        )

    def save(self, commit=True):
        """ Save instance and update BusStop if needed

        Args:
            commit (bool, optional): If commit==True changes are applied on database. Defaults to True.

        Returns:
            instance: BusShiftForm model instance created or updated
        """
        instance = super(BusShiftForm, self).save(commit=False)
        
        fields_dict = {
            'bus': instance.bus,
            'driver': instance.driver,
            'arrival': instance.arrival
        } 

        uid = uuid.UUID(str(instance.uid))

        # If busstop instance uid exists update BusStop
        if models.BusShift.objects.filter(uid=instance.uid).exists():
            # Get active bus shift and bus stop
            bus_shift = models.BusShift.objects.get(uid=instance.uid)
            bus_stop = models.BusStop.objects.get(pk=instance.bus_stop.pk)

            # Update bus shift and bus stop fields
            new_bus_shift = update_fields_instance(bus_shift, fields_dict, save=True)
            new_bus_stop = update_fields_instance(bus_stop, fields_dict, save=False)
            # Add bus stop foreign key

            new_bus_shift.bus_stop = new_bus_stop
            new_bus_shift.save()

        else:
            # If busstop instance uid doesn't exists create BusStop
            bus_stop = models.BusStop.objects.create(**fields_dict)
            instance.bus_stop_id = bus_stop.uid

        if commit:
            instance.uid = uid
            instance.save()
            
        return instance
