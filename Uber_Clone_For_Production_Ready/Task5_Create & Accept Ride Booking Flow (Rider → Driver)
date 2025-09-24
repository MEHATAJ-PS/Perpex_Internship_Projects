# -------------------------------
# rides/models.py
# -------------------------------
from django.db import models
from riders.models import Rider, Driver  # make sure riders app exists


class Ride(models.Model):
    STATUS_CHOICES = [
        ('REQUESTED', 'Requested'),
        ('ONGOING', 'Ongoing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    rider = models.ForeignKey(Rider, related_name='rides', on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, related_name='assigned_rides', on_delete=models.SET_NULL, null=True, blank=True)
    
    pickup_address = models.CharField(max_length=255)
    dropoff_address = models.CharField(max_length=255)
    pickup_lat = models.FloatField()
    pickup_lng = models.FloatField()
    drop_lat = models.FloatField()
    drop_lng = models.FloatField()
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='REQUESTED')
    requested_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ride {self.id} ({self.status})"


# -------------------------------
# rides/serializers.py
# -------------------------------
from rest_framework import serializers
from .models import Ride

class RideRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = [
            'pickup_address', 'dropoff_address',
            'pickup_lat', 'pickup_lng',
            'drop_lat', 'drop_lng'
        ]


class RideSerializer(serializers.ModelSerializer):
    rider = serializers.StringRelatedField()
    driver = serializers.StringRelatedField()

    class Meta:
        model = Ride
        fields = '__all__'


# -------------------------------
# rides/views.py
# -------------------------------
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Ride
from riders.models import Rider, Driver
from .serializers import RideRequestSerializer, RideSerializer

# Rider requests a ride
class RideRequestView(generics.CreateAPIView):
    serializer_class = RideRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            rider = self.request.user.rider_profile
        except Rider.DoesNotExist:
            raise PermissionError("Only riders can request rides")
        serializer.save(rider=rider, status='REQUESTED')


# Drivers view available rides
class AvailableRidesView(generics.ListAPIView):
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            driver = self.request.user.driver_profile
        except Driver.DoesNotExist:
            return Ride.objects.none()  # only drivers can view rides
        return Ride.objects.filter(status='REQUESTED', driver__isnull=True)


# Driver accepts a ride
class AcceptRideView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ride_id):
        try:
            driver = request.user.driver_profile
        except Driver.DoesNotExist:
            return Response({'error': 'Only drivers can accept rides'}, status=status.HTTP_403_FORBIDDEN)

        try:
            ride = Ride.objects.get(id=ride_id)
        except Ride.DoesNotExist:
            return Response({'error': 'Ride not found'}, status=status.HTTP_404_NOT_FOUND)

        if ride.status != 'REQUESTED' or ride.driver is not None:
            return Response({'error': 'Ride already accepted'}, status=status.HTTP_400_BAD_REQUEST)

        ride.driver = driver
        ride.status = 'ONGOING'
        ride.save()
        return Response({'message': 'Ride accepted successfully'})


# -------------------------------
# rides/urls.py
# -------------------------------
from django.urls import path
from .views import RideRequestView, AvailableRidesView, AcceptRideView

urlpatterns = [
    path('ride/request/', RideRequestView.as_view(), name='ride-request'),
    path('ride/available/', AvailableRidesView.as_view(), name='ride-available'),
    path('ride/accept/<int:ride_id>/', AcceptRideView.as_view(), name='ride-accept'),
]


# -------------------------------
# project urls.py (main)
# -------------------------------
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # JWT endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Ride endpoints
    path('api/rides/', include('rides.urls')),
]
