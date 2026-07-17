from django.contrib import admin
from .models import Amenity, Sport, TimeSlot, Turf, TurfImage

class TimeSlotInline(admin.TabularInline):
    model = TimeSlot
    extra = 1


class TurfImageInline(admin.TabularInline):
    model = TurfImage
    extra = 1


@admin.register(Turf)
class TurfAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "owner", "base_price", "is_active", "is_featured")
    list_filter = ("is_active", "is_featured", "city", "sports")
    search_fields = ("name", "city", "area", "owner__username")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("sports", "amenities")
    inlines = (TimeSlotInline, TurfImageInline)


admin.site.register([Sport, Amenity, TurfImage, TimeSlot])
