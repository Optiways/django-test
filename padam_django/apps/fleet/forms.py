# System import
import uuid

# Django import.
from django import forms

# App import.
from . import models
from .validators import is_bus_shift_slot_valid, is_bus_time_stop_slot_valid
from .utils import update_fields_instance, update_bus_shift, get_bus_shift_time

class BusShiftForm(forms.ModelForm):
    """ Form that allow to modify and create BusShift instance

    Raises:
        forms.ValidationError: _description_
    """
    class Meta:
        model = models.BusShift
        exclude = ['']
    

    def clean(self):

        driver = self.data['driver']
        arrival = self.data['arrival']
        departure = self.data['departure']

        # driver = self.fields['driver']
        # arrival = self.fields['arrival']
        # departure = self.fields['departure']

        self.fields['arrival'].initial = models.BusStop.objects.filter(driver=driver).order_by='arrival'.first()
        # self.data['arrival'] = models.BusStop.objects.filter(driver=driver).order_by='arrival'.first()
        self.fields['travel_time'].initial = arrival - departure

        # Get form input
        departure = self.cleaned_data.get('departure')
        arrival = self.cleaned_data.get('arrival')
        bus = self.cleaned_data.get('bus')
        driver = self.cleaned_data.get('driver')

        # Verify bus shift validity
        is_bus_time_stop_slot_valid(
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

        bus, driver, arrival \
            = instance.bus, instance.driver, instance.arrival
        
        fields_dict = {
            'bus': bus,
            'driver': driver,
            'arrival': arrival
        } 

        uid = uuid.UUID(str(instance.uid))

        # If busstop instance uid exists update BusStop
        if models.BusShift.objects.filter(uid=instance.uid).exists():
            # Get active bus shift and bus stop
            bus_shift = models.BusShift.objects.get(uid=instance.uid)
            bus_stop = models.BusStop.objects.get(pk=instance.bus_stop.pk)
            print('GET ACTIVE SHIFT: OK')
            
            instance.uid = uid

            # Update bus shift and bus stop fields
            new_bus_shift = update_fields_instance(bus_shift, fields_dict, save=True)
            new_bus_stop = update_fields_instance(bus_stop, fields_dict, save=False)
            print('UPDATE MODEL: OK')
            
            # Add bus stop foreign key
            new_bus_shift.bus_stop = new_bus_stop
            new_bus_shift.save()
            print('SAVE MODEL: OK')

        else:
            # If busstop instance uid doesn't exists create BusStop
            bus_stop = models.BusStop.objects.create(**fields_dict)
            instance.bus_stop_id = bus_stop.uid

        if commit:
            instance.save()
            
        return instance


class BusStopForm(forms.ModelForm):
    """ Form that allow to modify and create BusShift instance

    Raises:
        forms.ValidationError: _description_
    """
    class Meta:
        model = models.BusStop
        exclude = ['']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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
        """ Save instance and update BusStop if needed

        IF bus shift instance  (uid) | (driver && bus) exists 
        THEN update existing BusShift instance
        ELSE create BusShift instance

        Args:
            commit (bool, optional): If commit==True changes are applied on database. Defaults to True.

        Returns:
            instance: BusShiftForm model instance created or updated
        """
        # Get instance 
        instance = super(BusStopForm, self).save(commit=False)

        # Get shift attributes
        bus, driver = instance.bus, instance.driver
        departure, arrival, travel_time = get_bus_shift_time(driver, bus)

        uid = uuid.UUID(str(instance.uid))
        
        # OPTI: get instance dict
        update_dict = {
            'uid': uid,
            'driver': driver,
            'bus': bus,
            'bus_stop': instance,
            'departure': departure, 
            'arrival': arrival,
            'travel_time': travel_time
        }

        print('update_dict', update_dict)

        update_dict_valid = {k: v for k, v in update_dict.items() if v is not None}

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
