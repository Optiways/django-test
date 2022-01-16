from django import forms
from .models import BusShift
from django.db import models
from django.core.exceptions import ValidationError


class BusShiftForm(forms.ModelForm):
    class Meta:
        model = BusShift
        fields = ["bus", "driver", "bus_stop"]

    def clean(self):
        """
        Form intended for the admin interface with special logic
        to handle the validation of the input data.
        Takes 3 params:
            - Bus instance
            - Driver instance
            - BusStop queryset
        Returns:
            - cleaned_data
        """
        super().clean()

        bus = self.cleaned_data.get("bus")
        driver = self.cleaned_data.get("driver")
        bus_stop = self.cleaned_data.get("bus_stop")

        if bus and driver and bus_stop:

            start_dt = bus_stop.aggregate(models.Min("time"))["time__min"]
            end_dt = bus_stop.aggregate(models.Max("time"))["time__max"]

            base_qs = BusShift.objects.filter(
                models.Q(
                    start_dt__lte=start_dt,
                    end_dt__gt=start_dt,
                    end_dt__lte=end_dt,
                )
                | models.Q(start_dt__lte=start_dt, end_dt__gte=end_dt)
                | models.Q(start_dt__gte=start_dt, end_dt__lte=end_dt)
                | models.Q(
                    start_dt__gte=start_dt,
                    start_dt__lt=end_dt,
                    end_dt__gte=end_dt,
                )
            )

            if base_qs.filter(bus=bus).exists():
                # TODO: Give the user the datetime range already used by this bus
                raise ValidationError(
                    "There is already a bus_shift with this bus at this period !"
                )

            if base_qs.filter(driver=driver).exists():
                # TODO: Give the user the datetime range already used by this driver
                raise ValidationError(
                    "This driver is already on another bus_shift at this moment !"
                )

        self.cleaned_data["start_dt"] = start_dt
        self.cleaned_data["end_dt"] = end_dt
        self.instance.start_dt = start_dt
        self.instance.end_dt = end_dt

        return self.cleaned_data
