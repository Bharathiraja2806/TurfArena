from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ("booking_date", "slot", "notes")
        widgets = {"booking_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}), "notes": forms.Textarea(attrs={"rows": 3, "class": "form-control"})}
