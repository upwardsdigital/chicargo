from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Country
from .services import EmailService

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


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ("id", "name", "code",)


class StaffUserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    country = CountrySerializer(many=False)

    class Meta:
        model = User
        fields = (
            "id", "first_name",
            "last_name",
            "username", "email",
            "groups", "country"
        )


class CreateStaffUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        style={'input_type': 'password'},
        label='password'
    )
    confirm_password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        style={'input_type': 'password'},
        label='confirm password'
    )
    group = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id", "first_name", "last_name",
            "username", "email", "password",
            "confirm_password", "country", "group",
        )

    def create(self, validated_data):
        groups_id = validated_data.pop('group', 0)
        groups = Group.objects.filter(id__in=[groups_id])
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError('Passwords mismatch')
        user = User.objects.create(is_staff=True, **validated_data)
        user.set_password(password)
        user.groups.add(*groups)
        user.save()
        data = {
            "email_subject": "Your credentials!",
            "email_body": f"Email: {user.email} \n"
                          f"Password: {password} \n",
            "to_email": user.email,
        }
        EmailService.send_email(data)
        return user
