from .models import Expense, Type
from rest_framework import serializers


class TypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Type
        fields = '__all__'


class ExpenseCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    type = TypeSerializer(many=False)

    class Meta:
        model = Expense
        fields = '__all__'
