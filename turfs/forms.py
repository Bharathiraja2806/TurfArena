from django import forms
from .models import TimeSlot, Turf


class TurfForm(forms.ModelForm):
    class Meta:
        model = Turf
        fields = (
            "name", "slug", "description", "address", "city", "area", "sports",
            "amenities", "capacity", "size", "rules", "base_price", "is_active", "is_featured",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "address": forms.Textarea(attrs={"rows": 2}),
            "rules": forms.Textarea(attrs={"rows": 3}),
            "sports": forms.CheckboxSelectMultiple(),
            "amenities": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name not in ("sports", "amenities", "is_active", "is_featured"):
                field.widget.attrs["class"] = "form-control"


class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ("start_time", "end_time", "price", "is_active")
        widgets = {
            "start_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "end_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        }
