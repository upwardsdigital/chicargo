from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers


User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        username = attrs.get('username', '')
        user = User.objects.get(username=username)
        data.update(
            {
                "group": user.groups.all().first().name
                if user.groups.all().exists() else ""
            }
        )
        return data


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ("id", "name",)
