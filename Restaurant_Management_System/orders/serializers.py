from rest_framework import serializers
from .models import Order
from products.models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "name", "price"]  # adjust fields to match your Item model


class OrderSerializer(serializers.ModelSerializer):
    order_items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "created_at", "total_amount", "status", "order_items"]
