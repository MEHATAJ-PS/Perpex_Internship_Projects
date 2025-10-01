from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "name", "price"]


class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(),
        source="item",
        write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ["id", "item", "item_id", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    unique_id = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ["unique_id", "created_at", "total_amount", "status", "order_items"]

    def create(self, validated_data):
        items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                item=item_data['item'],
                quantity=item_data.get('quantity', 1),
                price=item_data['item'].price  # snapshot
            )
        order.calculate_total()
        order.save()
        return order
