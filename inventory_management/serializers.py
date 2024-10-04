from .models import Products
from rest_framework import serializers


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ("product_id", "product_name", "stock_quantity")

    def create(self, validated_data):
        return Products(**validated_data).save()
