from django.contrib import admin
from .models import BusStop, BusShift

class BusStopInline(admin.TabularInline):
    model = BusStop
    extra = 10

class BusShiftAdmin(admin.ModelAdmin):
    inlines = [BusStopInline]

admin.site.register(BusShift, BusShiftAdmin)
