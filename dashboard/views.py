from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from bookings.models import Booking
from turfs.models import Turf


def home(request):
    turfs = Turf.objects.filter(is_active=True).prefetch_related("sports", "amenities")[:20]
    return render(request, "dashboard/home.html", {"featured": turfs})


@login_required
def dashboard(request):
    bookings = Booking.objects.filter(customer=request.user).select_related("turf", "slot")
    return render(request, "dashboard/dashboard.html", {"bookings": bookings[:5], "booking_count": bookings.count(), "confirmed_total": bookings.filter(status=Booking.Status.CONFIRMED).aggregate(total=Sum("total_amount"))["total"] or 0})
