# uber_app/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Ride, RideFeedback
from .serializers import RideFeedbackSerializer


class RideFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ride_id):
        # ✅ 1. Fetch the ride
        ride = get_object_or_404(Ride, id=ride_id)

        # ✅ 2. Ensure user is part of this ride
        if request.user != ride.rider and request.user != ride.driver:
            return Response(
                {"error": "You are not authorized to give feedback for this ride."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # ✅ 3. Ensure ride is completed
        if ride.status != "COMPLETED":
            return Response(
                {"error": "Ride is not completed yet."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ✅ 4. Prevent duplicate feedback
        if RideFeedback.objects.filter(ride=ride, submitted_by=request.user).exists():
            return Response(
                {"error": "You have already submitted feedback for this ride."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ✅ 5. Pass data to serializer
        serializer = RideFeedbackSerializer(
            data=request.data,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save(ride=ride)  # ride is forced here
            return Response(
                {"message": "Feedback submitted successfully."},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# uber_app/urls.py
from django.urls import path
from .views import RideFeedbackView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # JWT Authentication
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Feedback API
    path("api/ride/feedback/<int:ride_id>/", RideFeedbackView.as_view(), name="ride_feedback"),
]
