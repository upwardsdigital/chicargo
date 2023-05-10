from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import (
    CustomTokenObtainPairView, GroupListAPIView,
    CountryListAPIView, StaffUserListCreateAPIView,
    ReportListCreateAPIView, ReportRetrieveUpdateAPIView
)

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('roles/', GroupListAPIView.as_view(), name="roles"),
    path('countries/', CountryListAPIView.as_view(), name="countries"),
    path('staff/users/', StaffUserListCreateAPIView.as_view(), name="staff_user"),
    path('reports/', ReportListCreateAPIView.as_view(), name="report_list"),
    path('reports/<int:pk>/', ReportRetrieveUpdateAPIView.as_view(), name="report_retrieve")
]
