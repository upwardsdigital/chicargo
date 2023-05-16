from .models import Expense, Type
from rest_framework import viewsets, generics, permissions
from .serializers import TypeSerializer, ExpenseCreateUpdateSerializer, ExpenseSerializer
from accounts.pagination import CustomPageNumberPagination
from .filters import ExpenseFilter


class TypeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class ExpenseModelViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)
    pagination_class = CustomPageNumberPagination
    queryset = Expense.objects.all()
    filterset_class = ExpenseFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ExpenseSerializer
        else:
            return ExpenseCreateUpdateSerializer
