from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("reference", "booking", "amount", "method", "status", "paid_at")
    list_filter = ("status", "method")
    search_fields = ("booking__reference", "provider_reference")
