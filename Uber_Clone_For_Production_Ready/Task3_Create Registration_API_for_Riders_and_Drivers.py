from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Rider, Driver


class UserSerializer(serializers.ModelSerializer):
    """Handles User creation and ensures password is hashed."""
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )


class RiderRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Rider
        fields = ["user", "phone_number", "preferred_payment_method", "default_pickup_location"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = UserSerializer().create(user_data)
        rider = Rider.objects.create(user=user, **validated_data)
        return rider


class DriverRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Driver
        fields = [
            "user",
            "phone_number",
            "vehicle_make",
            "vehicle_model",
            "license_plate",
            "driver_license_number",
            "is_available",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = UserSerializer().create(user_data)
        driver = Driver.objects.create(user=user, **validated_data)
        return driver
