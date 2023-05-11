from rest_framework import serializers
from .models import Product, ProductType, Status
from accounts.serializers import StaffUserSerializer


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = '__all__'


class ProductTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductType
        fields = '__all__'


class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    author = StaffUserSerializer(many=False)
    status = StatusSerializer(many=False)
    type = ProductTypeSerializer(many=False)

    class Meta:
        model = Product
        fields = '__all__'

