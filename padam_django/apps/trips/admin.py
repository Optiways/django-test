from django.contrib import admin
from .models import BusStop, BusShift
from .forms import BusShiftForm


class BusShiftAdmin(admin.ModelAdmin):
    form = BusShiftForm
    list_display = ["bus", "driver", "start_time", "end_time", "duration"]
    search_fields = ["bus__licence_plate", "driver__user__username"]


admin.site.register(BusStop)
admin.site.register(BusShift, BusShiftAdmin)
