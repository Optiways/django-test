from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import ModelForm

from padam_django.apps.busshifts.models import BusStop, BusShift
from padam_django.apps.common.utils.time_utils import overlap


class BusShiftForm(ModelForm):
    class Meta:
        model = BusShift
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BusShiftForm, self).__init__(*args, **kwargs)
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

            # Check if the bus is already used.
            other_shifts = BusShift.objects.filter(Q(bus=bus) & ~Q(pk=self.instance.pk))
            for s in other_shifts:
                if overlap((s.get_start_time(), s.get_end_time()), (start, end)):
                    raise ValidationError(f"The bus {bus} is already used for these dates")

            # Check if the driver is already drive a bus at this date.
            other_shifts = BusShift.objects.filter(Q(driver=driver) & ~Q(pk=self.instance.pk))
            for s in other_shifts:
                if overlap((s.get_start_time(), s.get_end_time()), (start, end)):
                    raise ValidationError(f"The driver {driver} is already driving at theses dates")

        return self.cleaned_data


class BusShiftAdmin(admin.ModelAdmin):
    form = BusShiftForm


admin.site.register(BusShift, BusShiftAdmin)
admin.site.register(BusStop)
