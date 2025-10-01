# rides.py (single file example)
from django.db import models
from rest_framework import serializers, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from math import radians, sin, cos, sqrt, atan2

# ---------------------------
# Ride Model
# ---------------------------
class Ride(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
    ]

    pickup_lat = models.FloatField()
    pickup_lon = models.FloatField()
    drop_lat = models.FloatField()
    drop_lon = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    fare = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Optional fields to check ownership
    # driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driver_rides', null=True)
    # rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rider_rides', null=True)

    def __str__(self):
        return f"Ride {self.id} - {self.status}"

# ---------------------------
# Serializer with Fare Calculation
# ---------------------------
class RideFareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'fare', 'status']

    def update(self, instance, validated_data):
        # Only calculate fare if ride is completed
        if instance.status != "COMPLETED":
            raise serializers.ValidationError("Fare can only be calculated for completed rides.")

        # Prevent re-calculation if fare already exists
        if instance.fare is not None:
            return instance

        # ---------------------------
        # Haversine Distance
        # ---------------------------
        R = 6371  # Earth radius in km
        lat1, lon1 = instance.pickup_lat, instance.pickup_lon
        lat2, lon2 = instance.drop_lat, instance.drop_lon

        phi1, phi2 = radians(lat1), radians(lat2)
        delta_phi = radians(lat2 - lat1)
        delta_lambda = radians(lon2 - lon1)

        a = sin(delta_phi/2)**2 + cos(phi1) * cos(phi2) * sin(delta_lambda/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance_km = R * c

        # ---------------------------
        # Fare Calculation
        # ---------------------------
        base_fare = 50
        per_km_rate = 10
        surge_multiplier = 1.0  # Change to 1.5 for peak hours

        fare = base_fare + (distance_km * per_km_rate) * surge_multiplier

        # Save fare
        instance.fare = round(fare, 2)
        instance.save()
        return instance

# ---------------------------
# View to Calculate Fare
# ---------------------------
class CalculateFareView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # JWT auth enforced

    def post(self, request, ride_id):
        try:
            ride = Ride.objects.get(id=ride_id)
        except Ride.DoesNotExist:
            return Response({"message": "Ride not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check ride status
        if ride.status != "COMPLETED":
            return Response({"message": "Ride must be completed before fare calculation."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Optional: check ownership if you have driver/rider fields
        # user = request.user
        # if not (user == ride.driver or user == ride.rider or user.is_staff):
        #     return Response({"message": "You do not have permission to calculate this fare."},
        #                     status=status.HTTP_403_FORBIDDEN)

        # Check if fare is already set
        if ride.fare is not None:
            return Response({"message": "Fare already set.", "fare": ride.fare},
                            status=status.HTTP_400_BAD_REQUEST)

        # Calculate and save fare
        serializer = RideFareSerializer(instance=ride, data={}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "fare": ride.fare,
            "message": "Fare calculated and saved."
        }, status=status.HTTP_200_OK)

# ---------------------------
# Example URL Pattern
# ---------------------------
# from django.urls import path
# urlpatterns = [
#     path('api/ride/calculate-fare/<int:ride_id>/', CalculateFareView.as_view(), name='calculate-fare'),
# ]
