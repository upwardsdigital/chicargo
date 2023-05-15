from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Country, Report
from .pagination import CustomPageNumberPagination
from .serializers import CustomTokenObtainPairSerializer
from .serializers import (
    GroupSerializer, CountrySerializer,
    StaffUserSerializer, CreateStaffUserSerializer,
    ReportSerializer, ReportRetrieveSerializer, UpdateStaffUserSerializer
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
    pagination_class = CustomPageNumberPagination
    queryset = User.objects.filter(is_staff=True, is_superuser=False)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StaffUserSerializer
        elif self.request.method == 'POST':
            return CreateStaffUserSerializer


class StaffUserUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)
    queryset = User.objects.filter(is_staff=True)
    serializer_class = UpdateStaffUserSerializer


class StaffUserDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)
    queryset = User.objects.filter(is_staff=True)
    serializer_class = StaffUserSerializer


class ReportListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPageNumberPagination
    filterset_fields = (
        'name', 'author__country'
    )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReportRetrieveSerializer
        elif self.request.method == 'POST':
            return ReportSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
        )

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Report.objects.all()
        else:
            return Report.objects.filter(author=self.request.user)


class ReportRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReportRetrieveSerializer
        elif self.request.method == 'PUT':
            return ReportSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Report.objects.all()
        else:
            return Report.objects.filter(author=self.request.user)
