from django.contrib import admin
from django.db.models import Count

from . import models


@admin.register(models.Bus)
class BusAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Driver)
class DriverAdmin(admin.ModelAdmin):
    pass

class BusStopInline(admin.TabularInline):
    model = models.BusShift.bus_stops.through

@admin.register(models.BusStop)
class BusStopAdmin(admin.ModelAdmin):
    list_display = ["place", "pass_time"]
    fields = ["place", "pass_time"]

    class Meta:
        ordering = ('-pass_time',)

@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    list_display = ["bus", "driver", "departure", "arrival", "bus_stop_number", "bus_shift_delay"]
    inlines = [BusStopInline]
    exclude= ("bus_stops",)

    def bus_stop_number(self, obj):
        '''
            return all busStop numbers 
        '''
        return obj.bus_stop_count

    def bus_shift_delay(self, obj):
        '''
            return  delay of bus shift diff betwwen it's arrival and departure busStop
        '''
        return str(obj.arrival.pass_time - obj.departure.pass_time)

    def get_queryset(self, request):
        ''' annotate queryset of each BusSift with their busStop number's'''
        return super().get_queryset(request).annotate(
            bus_stop_count=Count('bus_stops__id')
        )
