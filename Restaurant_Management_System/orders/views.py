from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer


class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(customer=request.user).order_by("-created_at")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
