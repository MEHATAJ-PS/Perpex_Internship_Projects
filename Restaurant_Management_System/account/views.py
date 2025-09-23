from rest_framework import generics, permissions
from .serializers import UserProfileSerializer

class UserProfileUpdateView(generics.UpdateAPIView):
    """
    API endpoint for updating the authenticated user's profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Ensures users can only update their own profile
        return self.request.user
