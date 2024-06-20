from rest_framework.routers import DefaultRouter
from .views import BusViewSet, DriverViewSet

router = DefaultRouter()
router.register(r'buses', BusViewSet)
router.register(r'drivers', DriverViewSet)

urlpatterns = router.urls