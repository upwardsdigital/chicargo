from django.urls import path, include
from .views import ExpenseModelViewSet, TypeListCreateAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'expenses', ExpenseModelViewSet, basename="expenses")

urlpatterns = [
    path('expense/types/', TypeListCreateAPIView.as_view(), name="expense_types"),
    path('', include(router.urls)),
]
