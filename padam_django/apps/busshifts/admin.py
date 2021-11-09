from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import ModelForm

from padam_django.apps.busshifts.models import BusStop, BusShift
from padam_django.apps.common.utils.time_utils import overlap


class BusShiftForm(ModelForm):
    """Form that verifies the integrity of the bus shifts"""
    class Meta:
        model = BusShift
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BusShiftForm, self).__init__(*args, **kwargs)
        # Display stops sorted by time in the multi-select box.
        self.fields['stops'].queryset = BusStop.objects.order_by('time')

    def clean(self):
        stops = self.cleaned_data.get('stops')
        bus = self.cleaned_data.get('bus')
        driver = self.cleaned_data.get('driver')
        if stops:
            # Check the minimum number of bus stops.
            if stops.count() < 2:
                raise ValidationError('At least two stops are required.')

            start = stops.order_by('time').first().time
            end = stops.order_by('time').last().time
            other_shifts_for_bus = BusShift.objects.filter(Q(bus=bus) & ~Q(pk=self.instance.pk))
            other_shifts_for_driver = BusShift.objects.filter(Q(driver=driver) & ~Q(pk=self.instance.pk))

            # Check if the bus is already in use.
            for shift in other_shifts_for_bus:
                if overlap((shift.start_time, shift.end_time), (start, end)):
                    raise ValidationError(f"The bus {bus} is already used for these dates")
            # Check if the driver is already driving a bus on this date.
            for shift in other_shifts_for_driver:
                if overlap((shift.start_time, shift.end_time), (start, end)):
                    raise ValidationError(f"The driver {driver} is already driving at theses dates")

        return self.cleaned_data


class BusShiftAdmin(admin.ModelAdmin):
    form = BusShiftForm


admin.site.register(BusShift, BusShiftAdmin)
admin.site.register(BusStop)
