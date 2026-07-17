import uuid
from django.db import models
from bookings.models import Booking


class Payment(models.Model):
    class Method(models.TextChoices):
        UPI = "UPI", "UPI"
        CARD = "CARD", "Credit / Debit Card"
        CASH = "CASH", "Cash at venue"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        FAILED = "FAILED", "Failed"
        REFUNDED = "REFUNDED", "Refunded"

    reference = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    booking = models.OneToOneField(Booking, on_delete=models.PROTECT, related_name="payment")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=10, choices=Method.choices)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    provider_reference = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.reference} · {self.get_status_display()}"
