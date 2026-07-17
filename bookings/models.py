import uuid
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from turfs.models import TimeSlot, Turf


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"
        COMPLETED = "COMPLETED", "Completed"

    reference = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="bookings")
    turf = models.ForeignKey(Turf, on_delete=models.PROTECT, related_name="bookings")
    slot = models.ForeignKey(TimeSlot, on_delete=models.PROTECT, related_name="bookings")
    booking_date = models.DateField(db_index=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING, db_index=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-booking_date", "slot__start_time"]
        constraints = [models.UniqueConstraint(fields=["turf", "slot", "booking_date"], condition=models.Q(status__in=["PENDING", "CONFIRMED"]), name="unique_active_booking_slot")]
    def clean(self):
        if self.slot_id and self.turf_id and self.slot.turf_id != self.turf_id:
            raise ValidationError("The selected slot does not belong to this turf.")
    def __str__(self): return f"{self.reference} · {self.turf}"
