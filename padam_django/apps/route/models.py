from django.db import models
from django import forms
from django.db.models import UniqueConstraint, Q
from padam_django.apps.fleet.models import Bus
from padam_django.apps.fleet.models import Driver
from padam_django.apps.geography.models import Place


class BusShift(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='bus')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='driver')
    stops = models.ManyToManyField(Place, through='BusStop')

    @property
    def departure_place(self):
        return self.stops.all().order_by("busstop__stoptime").first()

    @property
    def arrival_place(self):
        return self.stops.all().order_by("busstop__stoptime").last()

    @property
    def departure_time(self):
        return BusStop.objects.get(stop=self.departure_place, busshift=self).stoptime

    @property
    def arrival_time(self):
        return BusStop.objects.get(stop=self.arrival_place, busshift=self).stoptime

    def stoptime_during_journey(self, stop_time):
        if self.departure_time < stop_time and self.arrival_time > stop_time:
            return True
        return False

    def __str__(self):
        return f"{self.departure_place} to {self.arrival_place}"

class BusStop(models.Model):
    stop = models.ForeignKey(Place, on_delete=models.CASCADE)
    busshift = models.ForeignKey(BusShift, on_delete=models.CASCADE)
    stoptime = models.TimeField()

    class Meta:
        ordering = ['stoptime']

    def clean(self):
        for busshift in BusShift.objects.filter(bus=self.busshift.bus):
            if busshift.stoptime_during_journey(self.stoptime):
                raise forms.ValidationError("The bus is already used at this time")
        
        for busshift in BusShift.objects.filter(driver=self.busshift.driver):
            if busshift.stoptime_during_journey(self.stoptime):
                raise forms.ValidationError("The driver is already working at this time")
        

class BusStopForm(forms.models.BaseInlineFormSet):
    def clean(self):
        busstop_count = 0
        for form in self.forms:
            if form.cleaned_data:
                busstop_count += 1
        if busstop_count < 2:
            raise forms.ValidationError("A bus shift must have at least two stops")

