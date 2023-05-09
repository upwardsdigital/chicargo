from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Country
from .serializers import CustomTokenObtainPairSerializer
from .serializers import (
    GroupSerializer, CountrySerializer, StaffUserSerializer, CreateStaffUserSerializer
)

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class GroupListAPIView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CountryListAPIView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class StaffUserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.filter(is_staff=True)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StaffUserSerializer
        elif self.request.method == 'POST':
            return CreateStaffUserSerializer
