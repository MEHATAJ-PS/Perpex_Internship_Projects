from rest_framework import serializers
from .models import (
    RestaurantInfo,
    Contact,
    SimpleContact,
    Feedback,
    RestaurantLocation,
)


class RestaurantInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantInfo
        fields = ["id", "name", "phone_number", "address", "opening_hours"]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["id", "name", "email", "submitted_at"]


class SimpleContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimpleContact
        fields = ["id", "name", "email", "submitted_at"]


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["id", "name", "email", "comments", "submitted_at"]


class RestaurantLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantLocation
        fields = ["id", "address", "city", "state", "pincode"]
