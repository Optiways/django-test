from django.db import models
from django.core.exceptions import ValidationError
from django import forms
from padam_django.apps.geography.models import BusStop


class Driver(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='driver')

    def __str__(self):
        return f"Driver: {self.user.username} (id: {self.pk})"


class Bus(models.Model):
    licence_plate = models.CharField("Name of the bus", max_length=10)

    class Meta:
        verbose_name_plural = "Buses"

    def __str__(self):
        return f"Bus: {self.licence_plate} (id: {self.pk})"


class BusShift(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='shifts')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='shifts')
    start = models.DateTimeField("Start of the shift")
    end = models.DateTimeField("End of the shift")
    bus_stop_ids = models.TextField(blank=True, default='[]')

    class Meta:
        ordering = ['start']

    def __str__(self):
        return f"BusShift: {self.bus.licence_plate} (Driver: {self.driver.user.username}, Start: {self.start}, End: {self.end})"


class BusShiftForm(forms.ModelForm):
    bus_stop_ids = forms.CharField(widget=forms.Textarea, help_text="Enter bus stop IDs separated by commas")

    class Meta:
        model = BusShift
        fields = ['bus', 'driver', 'start', 'end', 'bus_stop_ids']

    def clean_bus_stop_ids(self):
        bus_stop_ids = self.cleaned_data['bus_stop_ids']
        bus_stop_ids = [int(id.strip()) for id in bus_stop_ids.split(',') if id.strip().isdigit()]

        if len(bus_stop_ids) < 2:
            raise ValidationError("There must be at least two stops.")

        # Ensure all bus stop IDs are valid
        if not BusStop.objects.filter(id__in=bus_stop_ids).count() == len(bus_stop_ids):
            raise ValidationError("One or more bus stop IDs are invalid.")

        return bus_stop_ids

    def clean(self):
        cleaned_data = super().clean()
        bus = cleaned_data.get('bus')
        driver = cleaned_data.get('driver')
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')

        # Ensure the end time is after the start time
        if start and end and start >= end:
            raise ValidationError("The end time must be after the start time.")

        # Ensure no overlapping shifts for the same bus
        if bus and start and end:
            overlapping_bus_shifts = BusShift.objects.filter(
                bus=bus,
                start__lt=end,
                end__gt=start
            ).exclude(pk=self.instance.pk)
            if overlapping_bus_shifts.exists():
                raise ValidationError("The bus has overlapping shifts.")

        # Ensure no overlapping shifts for the same driver
        if driver and start and end:
            overlapping_driver_shifts = BusShift.objects.filter(
                driver=driver,
                start__lt=end,
                end__gt=start
            ).exclude(pk=self.instance.pk)
            if overlapping_driver_shifts.exists():
                raise ValidationError("The driver has overlapping shifts.")

        return cleaned_data