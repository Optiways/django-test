from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import query
from django.db.models.fields import related, reverse_related
from padam_django.apps.fleet.models import Bus
from datetime import datetime, date

class BusShift(models.Model):
    bus = models.ForeignKey("fleet.Bus", on_delete=models.PROTECT)
    driver = models.ForeignKey("fleet.Driver", on_delete=models.PROTECT)
    stops = models.ManyToManyField("BusStop")
    departure_stop = models.ForeignKey("BusStopTime", on_delete=models.PROTECT, related_name='departure_stop', null=True)
    arrival_stop = models.ForeignKey("BusStopTime", on_delete=models.PROTECT, related_name='arrival_stop', null=True)

    def total_time(self):
        time = datetime.combine(date.today(), self.arrival_stop.time) - datetime.combine(date.today(), self.departure_stop.time)
        return str(int(time.seconds / 60)) + ' minutes'

    def check_availability(self, queryset, error_message):
        for shifts in queryset:
            if shifts.departure_stop.time <= self.departure_stop.time <= shifts.arrival_stop.time:
                raise ValidationError(error_message) 
            if shifts.departure_stop.time <= self.arrival_stop.time <= shifts.departure_stop.time:
                raise ValidationError(error_message)
            if self.arrival_stop.time > shifts.departure_stop.time and self.departure_stop.time < shifts.departure_stop.time:
                raise ValidationError(error_message)
        
    def clean(self):
        # checking user input regarding times
        if self.departure_stop.time == self.arrival_stop.time:
            raise ValidationError("Dates are incorrect - departure time cannot be similar of arrival time")
        if self.departure_stop.time > self.arrival_stop.time:
            raise ValidationError("Dates are incorrect - departure time cannot be ahead of arrival time")

        # checking user input regarding bus availability 
        queryset_bus = BusShift.objects.all().filter(bus=self.bus).exclude(pk=self.id)
        queryset_driver = BusShift.objects.all().filter(driver=self.driver).exclude(pk=self.id)
        self.check_availability(queryset_bus, "This bus is already on a shift at those times.")
        self.check_availability(queryset_driver, "This driver is already on a shift at those times.")

    def __str__(self):
        return f"BusShift: {self.driver.user} driving {self.bus.licence_place} from {self.departure_stop.stop.name} to {self.arrival_stop.stop.name} for {self.total_time()}"

class BusStop(models.Model):
    name = models.CharField('Bus stop name', max_length=100)
    place = models.ForeignKey("geography.Place", on_delete=models.CASCADE)

    def __str__(self):
        return f"BusStop: {self.name} @ {self.place.name}"

class BusStopTime(models.Model):
    stop = models.ForeignKey("BusStop", on_delete=models.CASCADE)
    time = models.TimeField(auto_now=False, null=True)

    def __str__(self):
        return f"BusStopTime: {self.stop.name} at {self.time}"