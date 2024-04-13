"""padam_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .api.bus.view import BusViewSet
from .api.bus_shift.views import BusShiftViewSet
from .api.driver.views import DriverViewSet
from .api.user.views import UserViewSet
from .api.stop.views import BusStopViewSet

router = routers.DefaultRouter()
router.register(r'buses', BusViewSet)
router.register(r'bus_shifts', BusShiftViewSet)
router.register(r'drivers', DriverViewSet)
router.register(r'users', UserViewSet)
router.register(r'stops', BusStopViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
