from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)

    @action(detail=True, methods=['delete'], url_path='cancel')
    def cancel_order(self, request, pk=None):
        try:
            order = self.get_queryset().get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if order.status in ['cancelled']:
            return Response({"error": "Order is already cancelled"}, status=status.HTTP_400_BAD_REQUEST)

        if order.status in ['delivered']:
            return Response({"error": "Delivered orders cannot be cancelled"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = 'cancelled'
        order.save()
        serializer = self.get_serializer(order)
        return Response({"message": "Order cancelled successfully", "order": serializer.data}, status=status.HTTP_200_OK)


class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(customer=request.user).order_by("-created_at")
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_orders = paginator.paginate_queryset(orders, request)
        serializer = OrderSerializer(paginated_orders, many=True)
        return paginator.get_paginated_response(serializer.data)

