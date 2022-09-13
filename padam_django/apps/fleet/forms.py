# System import
from sqlite3 import IntegrityError
import uuid

# Django import.
from django import forms

# App import.
from . import models
from .validators import is_bus_time_stop_slot_valid
from .utils import get_bus_shift_time
from .utils import get_update_instance_dict

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
        cleaned_data = super(BusStopForm, self).clean()
        # Get form input
        driver = cleaned_data.get('driver')
        bus = cleaned_data.get('bus')

        time_stop = cleaned_data.get('time_stop')
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
            (bus shift instance uid) | (driver && bus && departure__date) exists 
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
        # Get BusStop instance from BusStopForm 
        instance = super(BusStopForm, self).save(commit=False)

        # Get shift attributes
        bus, driver, time_stop = instance.bus, instance.driver, instance.time_stop
        departure, arrival, travel_time = get_bus_shift_time(driver, bus, time_stop)
        date = str(departure.date())
        print('---> date', date)
        uid = uuid.UUID(str(instance.uid))
        
        bus_shift_input_dict = {
            'bus_stop_id': instance.uid,
            'departure': departure,
            'arrival': arrival,
            'travel_time': travel_time,
            'date': date
        }

        update_dict = get_update_instance_dict(instance, bus_shift_input_dict)
        print('input_dict', update_dict)
        
        if models.BusStop.objects.filter(uid=uid).exists():
            print('---> UPDATE BUS SHIFT INSTANCE BY BUS STOP UID')
            new_bus_shift_instance = models.BusShift.objects.update(**update_dict)
            #     bus_stop_id=instance.uid,
            #     departure=departure,
            #     driver=driver, 
            #     bus=bus, 
            #     date=departure.date()
            # )      
        # IF bus_stop_id foreign key instance exists
        elif models.BusShift.objects.filter(bus_stop_id=instance.uid).exists():
            # THEN update it
            print('---> UPDATE BUS SHIFT INSTANCE BY BUS STOP UID')
            new_bus_shift_instance = models.BusShift.objects.update(
                bus_stop_id=instance.uid,
                driver=driver, 
                bus=bus, 
                departure=departure,
                arrival=arrival,
                travel_time=travel_time,
                date=date
            )

        # IF BusShift instance with same driver, same bus and same date exists
        elif models.BusShift.objects.filter(
            driver=driver, 
            bus=bus, 
            date=date
        ).exists():
            # THEN get this instance and create another foreign key for bus_stop 
            print('---> UPDATE BUS SHIFT INSTANCE')
            print('travel_time', travel_time)
            try:
                new_bus_shift_instance = models.BusShift.objects.get(
                    driver=driver,
                    bus=bus,
                    date=date,
                )
                assert new_bus_shift_instance is not None
                if new_bus_shift_instance is not None:
                    new_bus_shift_instance.bus_stop_id = instance.uid
                    new_bus_shift_instance.departure = departure
                    new_bus_shift_instance.arrival = arrival
                    new_bus_shift_instance.travel_time = travel_time
                    new_bus_shift_instance.save()

                assert new_bus_shift_instance.travel_time is not None
            except Exception as exc:
                print(exc)
                raise forms.ValidationError('Bus Shift could not be updated !')


        else:
            try:
                print('---> CREATE BUS SHIFT INSTANCE')
                bus_shift_instance = models.BusShift.objects.create(**update_dict)
                bus_shift_instance.save()
            except Exception as exc:
                print(exc)
                raise forms.ValidationError('Bus Shift could not be created !')
    
#     instance.bus_stop_id = instance.uid
#     instance.departure = departure
#     instance.arrival = arrival
#     instance.travel_time = arrival - instance

        # update_or_create_bus_shift(
        #     instance=existing_bus_shift_instance, 
        #     departure=departure, 
        #     arrival=arrival
        # )

        if commit:
            instance.save()
   
        return instance