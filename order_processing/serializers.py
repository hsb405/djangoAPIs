from .models import Order
from rest_framework import serializers


class OrderSerializer(serializers.Serializer):

    class Meta:
        model = Order
        fields = (
            "order_id",
            "customer_name",
            "product_name",
            "quantity",
            "delivery_address",
            "order_status",
            "created_at",
        )

    def create(self, validated_data):
        return Order(**validated_data).save()
