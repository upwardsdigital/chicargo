from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from django.utils.translation import gettext as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import IntegrityError
from rest_framework.utils import model_meta


from .models import Country, Report
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
                if user.groups.all().exists() else "",
                "full_name": user.full_name,
                "email": user.email,
                "username": user.username,
                "country": {
                    "id": user.country.id if user.country is not None else 0,
                    "name": user.country.name if user.country is not None else "",
                }
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
            "id", "full_name",
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
            "id", "full_name",
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
        # EmailService.send_email(data)
        return user


class UpdateStaffUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        style={'input_type': 'password'},
        label='password',
        required=False,
        allow_blank=True
    )
    confirm_password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        style={'input_type': 'password'},
        label='confirm password',
        required=False,
        allow_blank=True
    )
    group = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id", "full_name",
            "username", "email", "password",
            "confirm_password", "country", "group",
        )

    def update(self, instance, validated_data):
        group_id = validated_data.get('group', 0)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.country = validated_data.get('country', instance.country)
        groups = Group.objects.filter(id__in=[group_id])
        instance.groups.clear()
        instance.groups.add(*groups)
        password = validated_data.pop("password", "")
        confirm_password = validated_data.pop("confirm_password", "")
        if password != "" and confirm_password != "":
            if password != confirm_password:
                raise serializers.ValidationError(
                    {
                        "message": {
                            "password": [
                                _("Passwords mismatch")
                            ],
                            "status": 400
                        }
                    }
                )
            instance.set_password(password)
        try:
            instance.save()
        except IntegrityError as e:
            raise serializers.ValidationError(
                {
                    "message": {
                        "username": [
                            _("User with this username already exists.")
                        ],
                        "status": 400
                    }
                }
            )
        instance.save()
        return instance


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = '__all__'

    def create(self, validated_data):
        info = model_meta.get_field_info(self.Meta.model)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)
        instance, created = self.Meta.model.objects.update_or_create(
            name=validated_data.get("name", None),
            defaults=validated_data
        )
        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                if created:
                    field.set(value)
                else:
                    field.add(*value)
        return instance


class ReportRetrieveSerializer(serializers.ModelSerializer):
    users = StaffUserSerializer(many=True)

    class Meta:
        model = Report
        fields = '__all__'
