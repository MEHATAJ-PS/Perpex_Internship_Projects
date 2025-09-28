from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import Order
from .serializers import OrderSerializer


class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(customer=request.user).order_by("-created_at")

        # Add pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # adjust as needed
        paginated_orders = paginator.paginate_queryset(orders, request)

        serializer = OrderSerializer(paginated_orders, many=True)
        return paginator.get_paginated_response(serializer.data)

