from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from bookings.models import Booking
from .forms import PaymentMethodForm
from .models import Payment


@login_required
def checkout(request, reference):
    booking = get_object_or_404(Booking.objects.select_related("turf", "slot"), reference=reference, customer=request.user)
    if booking.status == Booking.Status.CANCELLED:
        messages.error(request, "Cancelled bookings cannot be paid for.")
        return redirect("bookings:history")
    existing_payment = getattr(booking, "payment", None)
    if existing_payment and existing_payment.status == Payment.Status.PAID:
        return redirect("payments:success", reference=booking.reference)
    form = PaymentMethodForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            payment, _ = Payment.objects.update_or_create(
                booking=booking,
                defaults={"amount": booking.total_amount, "method": form.cleaned_data["method"], "status": Payment.Status.PAID, "paid_at": timezone.now(), "provider_reference": f"TA-{booking.reference.hex[:10].upper()}"},
            )
            booking.status = Booking.Status.CONFIRMED
            booking.save(update_fields=["status"])
        messages.success(request, "Payment received. Your booking is confirmed!")
        return redirect("payments:success", reference=booking.reference)
    return render(request, "payments/checkout.html", {"booking": booking, "form": form})


@login_required
def success(request, reference):
    booking = get_object_or_404(Booking.objects.select_related("turf", "slot", "payment"), reference=reference, customer=request.user)
    return render(request, "payments/success.html", {"booking": booking})
