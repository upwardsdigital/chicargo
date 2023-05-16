from django.urls import path
from .views import TruckListCreateAPIView


urlpatterns = [
    path('trucks/', TruckListCreateAPIView.as_view(), name="trucks")
]
