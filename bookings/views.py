from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render
from turfs.models import Turf
from .forms import BookingForm
from .models import Booking


@login_required
def create_booking(request, slug):
    turf = get_object_or_404(Turf, slug=slug, is_active=True)
    form = BookingForm(request.POST or None)
    form.fields["slot"].queryset = turf.slots.filter(is_active=True)
    if request.method == "POST" and form.is_valid():
        booking = form.save(commit=False)
        booking.customer, booking.turf = request.user, turf
        booking.total_amount = booking.slot.price or turf.base_price
        try:
            with transaction.atomic():
                booking.full_clean()
                booking.save()
        except IntegrityError:
            form.add_error(None, "That slot has just been reserved. Please select another time.")
        else:
            messages.success(request, "Booking created. Complete payment to confirm it.")
            return redirect("payments:checkout", reference=booking.reference)
    return render(request, "bookings/create.html", {"form": form, "turf": turf})


@login_required
def history(request):
    bookings = Booking.objects.filter(customer=request.user).select_related("turf", "slot")
    return render(request, "bookings/history.html", {"bookings": bookings})
