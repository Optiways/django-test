from django.urls import path

from padam_django.apps.fleet import views

app_name = 'fleet'

urlpatterns = [
    path('shifts/', views.BusShiftListView.as_view(), name='bus_shift_all'),
    path('shifts/create/', views.BusShiftCreateView.as_view(), name='bus_shift_create'),
    path('shifts/update/<int:pk>/', views.BusShiftUpdateView.as_view(), name='bus_shift_update'),
    path('shifts/delete/<int:pk>/', views.BusShiftDeleteView.as_view(), name='bus_shift_delete')
]
