from rest_framework import serializers, viewsets
from bookings.models import Booking
from turfs.models import Turf


class TurfSerializer(serializers.ModelSerializer):
    sports = serializers.StringRelatedField(many=True)
    class Meta:
        model = Turf
        fields = ("id", "name", "slug", "city", "area", "base_price", "sports", "is_featured")


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ("reference", "turf", "slot", "booking_date", "total_amount", "status")
        read_only_fields = fields


class TurfViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Turf.objects.filter(is_active=True).prefetch_related("sports")
    serializer_class = TurfSerializer


class BookingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BookingSerializer
    def get_queryset(self): return Booking.objects.filter(customer=self.request.user).select_related("turf", "slot")
