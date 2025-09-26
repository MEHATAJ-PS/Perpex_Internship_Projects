# uber_app/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Ride

# ----------------------------
# Complete Ride (Driver Only)
# ----------------------------
class CompleteRideView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ride_id):
        try:
            ride = Ride.objects.get(id=ride_id)
        except Ride.DoesNotExist:
            return Response({"error": "Ride not found."}, status=status.HTTP_404_NOT_FOUND)

        # Only driver assigned can complete
        if ride.driver != getattr(request.user, "driver_profile", None):
            return Response({"error": "You are not the assigned driver for this ride."},
                            status=status.HTTP_403_FORBIDDEN)

        # Ride must be ongoing
        if ride.status != "ONGOING":
            return Response({"error": "Only ongoing rides can be completed."},
                            status=status.HTTP_400_BAD_REQUEST)

        ride.status = "COMPLETED"
        ride.save()
        return Response({"message": "Ride marked as completed."}, status=status.HTTP_200_OK)


# ----------------------------
# Cancel Ride (Rider Only)
# ----------------------------
class CancelRideView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ride_id):
        try:
            ride = Ride.objects.get(id=ride_id)
        except Ride.DoesNotExist:
            return Response({"error": "Ride not found."}, status=status.HTTP_404_NOT_FOUND)

        # Only rider who booked can cancel
        if ride.rider != getattr(request.user, "rider_profile", None):
            return Response({"error": "You are not the rider who booked this ride."},
                            status=status.HTTP_403_FORBIDDEN)

        # Can cancel only if still requested
        if ride.status != "REQUESTED":
            return Response({"error": "Cannot cancel a ride that is already ongoing or completed."},
                            status=status.HTTP_400_BAD_REQUEST)

        ride.status = "CANCELLED"
        ride.save()
        return Response({"message": "Ride cancelled successfully."}, status=status.HTTP_200_OK)

# uber_app/urls.py
from django.urls import path
from .views import CompleteRideView, CancelRideView

urlpatterns = [
    path("api/ride/complete/<int:ride_id>/", CompleteRideView.as_view(), name="ride-complete"),
    path("api/ride/cancel/<int:ride_id>/", CancelRideView.as_view(), name="ride-cancel"),
]
