# uber_app/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Ride(models.Model):
    STATUS_CHOICES = [
        ("REQUESTED", "Requested"),
        ("ONGOING", "Ongoing"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]
    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rides_as_rider")
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="rides_as_driver")
    pickup = models.CharField(max_length=255)
    drop = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="REQUESTED")
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ride {self.id} - {self.rider.username} ({self.status})"


class RideFeedback(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name="feedbacks")
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    is_driver = models.BooleanField()  # True = driver left feedback, False = rider
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("ride", "submitted_by")  # ensures 1 feedback per user per ride

    def __str__(self):
        return f"Feedback by {self.submitted_by.username} (Driver={self.is_driver})"


# uber_app/serializers.py
from rest_framework import serializers
from .models import Ride, RideFeedback


class RideFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideFeedback
        fields = ["id", "ride", "rating", "comment", "is_driver", "submitted_at"]
        read_only_fields = ["id", "submitted_at", "is_driver"]

    def validate(self, data):
        request = self.context["request"]
        user = request.user
        ride = data.get("ride")

        # ✅ Ensure ride belongs to user (rider or driver)
        if not (ride.rider == user or ride.driver == user):
            raise serializers.ValidationError("You are not part of this ride.")

        # ✅ Ensure ride is completed
        if ride.status != "COMPLETED":
            raise serializers.ValidationError("Ride is not completed yet.")

        # ✅ Prevent duplicate feedback
        if RideFeedback.objects.filter(ride=ride, submitted_by=user).exists():
            raise serializers.ValidationError("Feedback already submitted.")

        return data

    def create(self, validated_data):
        user = self.context["request"].user
        ride = validated_data["ride"]

        # Identify if feedback is from driver or rider
        is_driver = ride.driver == user
        validated_data["submitted_by"] = user
        validated_data["is_driver"] = is_driver

        return super().create(validated_data)
