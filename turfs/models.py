from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Sport(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=50, blank=True)
    def __str__(self): return self.name


class Amenity(models.Model):
    name = models.CharField(max_length=80, unique=True)
    def __str__(self): return self.name


class Turf(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="turfs")
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True)
    description = models.TextField()
    address = models.TextField()
    city = models.CharField(max_length=80, db_index=True)
    area = models.CharField(max_length=80, blank=True, db_index=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    sports = models.ManyToManyField(Sport, related_name="turfs")
    amenities = models.ManyToManyField(Amenity, blank=True, related_name="turfs")
    capacity = models.PositiveIntegerField(default=10)
    size = models.CharField(max_length=80, blank=True)
    rules = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-is_featured", "name"]
    def __str__(self): return self.name


class TurfImage(models.Model):
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="turfs/")
    alt_text = models.CharField(max_length=150, blank=True)
    is_cover = models.BooleanField(default=False)


class TimeSlot(models.Model):
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE, related_name="slots")
    start_time = models.TimeField()
    end_time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        ordering = ["start_time"]
        constraints = [models.UniqueConstraint(fields=["turf", "start_time", "end_time"], name="unique_turf_slot")]
    def __str__(self): return f"{self.turf}: {self.start_time}-{self.end_time}"
