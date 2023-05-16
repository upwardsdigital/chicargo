from rest_framework import serializers
from .models import Truck
from orders.serializers import ProductSerializer
from orders.models import Product


class TruckCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Truck
        fields = '__all__'

    def create(self, validated_data):
        instance = Truck.objects.create(**validated_data)
        products = Product.objects.filter(status__slug="loading")
        for product in products:
            product.truck = instance
            product.save()
        return instance


class TruckSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Truck
        fields = (
            'id', 'full_name',
            'volume', 'products',
            'count_of_products',
            'created_at',
        )
