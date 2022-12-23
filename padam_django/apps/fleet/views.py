from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from .forms import BusShiftForm
from .models import BusShift


class BusShiftView(View):
    model = BusShift
    success_url = reverse_lazy('fleet:bus_shift_all')


class BusShiftListView(BusShiftView, ListView):
    """View to list all BusShifts"""
    template_name = 'fleet/list.html'


class BusShiftCreateView(BusShiftView, CreateView):
    """View to create a new BusShift"""
    form_class = BusShiftForm
    template_name = 'fleet/create.html'


class BusShiftUpdateView(BusShiftView, UpdateView):
    """View to update a BusShift"""
    form_class = BusShiftForm
    template_name = 'fleet/update.html'


class BusShiftDeleteView(BusShiftView, DeleteView):
    """View to delete a BusShift"""
    template_name = 'fleet/delete.html'
