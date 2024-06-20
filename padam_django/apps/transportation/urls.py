from rest_framework.routers import DefaultRouter
from .views import BusStopViewSet, BusShiftViewSet

router = DefaultRouter()
router.register(r'busstops', BusStopViewSet)
router.register(r'busshifts', BusShiftViewSet)

urlpatterns = router.urls