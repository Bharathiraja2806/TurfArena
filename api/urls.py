from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, TurfViewSet
router = DefaultRouter()
router.register("turfs", TurfViewSet)
router.register("bookings", BookingViewSet, basename="booking")
urlpatterns = [path("", include(router.urls))]
