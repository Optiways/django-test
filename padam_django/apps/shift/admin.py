from django.contrib import admin

from .models import BusStop, BusStopTime, BusShift

admin.site.register(BusStop)
admin.site.register(BusStopTime)
admin.site.register(BusShift)
