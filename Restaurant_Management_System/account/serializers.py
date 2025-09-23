from django.contrib.auth.models import User
from rest_framework import serializers

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]  # Editable fields only
        extra_kwargs = {
            "email": {"required": True},
        }
