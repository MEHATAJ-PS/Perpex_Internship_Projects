from django.db import models
from django.contrib.auth.models import User


class Rider(models.Model):
    """
    Rider profile model extending the base Django User.
    Stores rider-specific details like phone, payment method, and saved location.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="rider_profile")
    phone_number = models.CharField(max_length=15, unique=True)
    preferred_payment_method = models.CharField(max_length=50, blank=True, null=True)
    default_pickup_location = models.CharField(max_length=255, blank=True, null=True)
    profile_photo = models.ImageField(upload_to="riders/", blank=True, null=True)

    def __str__(self):
        return f"Rider: {self.user.username}"


class Driver(models.Model):
    """
    Driver profile model extending the base Django User.
    Stores driver-specific details like vehicle, license, and availability.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="driver_profile")
    phone_number = models.CharField(max_length=15, unique=True)
    vehicle_make = models.CharField(max_length=50, blank=True, null=True)
    vehicle_model = models.CharField(max_length=50, blank=True, null=True)
    license_plate = models.CharField(max_length=20, unique=True, blank=True, null=True)
    driver_license_number = models.CharField(max_length=50, unique=True)
    is_available = models.BooleanField(default=True)
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    profile_photo = models.ImageField(upload_to="drivers/", blank=True, null=True)

    def __str__(self):
        return f"Driver: {self.user.username} - {self.license_plate or 'No Vehicle'}"
