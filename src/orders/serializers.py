from rest_framework import serializers
from .models import Product, ProductType, Status, PackageType
from accounts.serializers import StaffUserSerializer


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = '__all__'


class ProductTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductType
        fields = '__all__'


class PackageTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PackageType
        fields = '__all__'


class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    author = StaffUserSerializer(many=False)
    status = StatusSerializer(many=False)
    type = ProductTypeSerializer(many=False)
    package_type = PackageTypeSerializer(many=False)

    class Meta:
        model = Product
        fields = '__all__'

