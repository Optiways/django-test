# System import
import uuid

# Django import.
from django import forms

# App import.
from . import models
from .validators import is_bus_time_stop_slot_valid
from .utils import update_bus_shift, get_bus_shift_time
from .utils import update_instance_dict

class BusStopForm(forms.ModelForm):
    """ Form that allow to modify and create BusStop instance and create or update BusShift automatically

    Args:
        forms (instance): Instance to create the ModelForm (BusStop)

    Raises:
        forms.ValidationError: Raise form error if time_stop format is invalid
        forms.ValidationError: Raise form error if BusShift could not be created 

    Returns:
        BusStop: BusStop instance
    """
    class Meta:
        model = models.BusStop
        exclude = ['']

    def clean(self):
        # Get form input
        driver = self.cleaned_data.get('driver')
        bus = self.cleaned_data.get('bus')
        time_stop = self.cleaned_data.get('time_stop')
        if time_stop is None:
            raise forms.ValidationError('Time stop is incorrect')

        # Verify bus shift validity
        is_bus_time_stop_slot_valid(
            driver=driver,
            bus=bus,
            new_time_stop=time_stop, 
        )

    def save(self, commit=True):
        """ Save form instance model and update BusStop if needed in database

        IF 
            bus shift instance  (uid) | (driver && bus) exists 
        THEN 
            update existing BusShift instance
        ELSE 
            create BusShift instance

        Args:
            commit (bool, optional): 
                Persist changes in database. Defaults to True.

        Returns:
            instance: BusShiftForm model instance created or updated
        """
        # Get instance 
        instance = super(BusStopForm, self).save(commit=False)

        # Get shift attributes
        bus, driver = instance.bus, instance.driver
        departure, arrival, travel_time = get_bus_shift_time(driver, bus)
        uid = uuid.UUID(str(instance.uid))
        
        input_dict = {
            'uid': uid,
            'bus_stop': instance,
            'departure': departure,
            'arrival': arrival,
            'travel_time': travel_time
        }

        print('input_dict', input_dict)

        new_instance_dict = update_instance_dict(instance, input_dict)

        update_dict_valid = {k: v for k, v in new_instance_dict.items() if v is not None}

        if not models.BusShift.objects.filter(uid=instance.uid).exists():
            bus_shift_instance = models.BusShift.objects.create(**update_dict_valid)
            bus_shift_instance.save()
        
        else:
            if models.BusShift.objects.filter(uid=instance.uid).exists():
                existing_bus_shift_instance = models.BusShift.objects.get(uid=uid)

            elif models.BusShift.objects.filter(driver=driver, bus=bus).exists():
                existing_bus_shift_instance = models.BusShift.objects.get(driver=driver, bus=bus)

            else:
                raise forms.ValidationError('Bus Shift cannot be created !')

            update_bus_shift(
                instance=existing_bus_shift_instance, 
                departure=departure, 
                arrival=arrival
            )

        if commit:
            instance.save()
            
        return instance
