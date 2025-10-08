from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'bookings', BookingViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = router.urls
