from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer
from django.contrib.auth.models import Group
from rest_framework import generics
from .serializers import GroupSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class GroupListAPIView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
