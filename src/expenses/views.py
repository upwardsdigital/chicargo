from .models import Expense, Type
from rest_framework import viewsets, generics
from .serializers import TypeSerializer, ExpenseCreateUpdateSerializer, ExpenseSerializer
from accounts.pagination import CustomPageNumberPagination


class TypeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class ExpenseModelViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPageNumberPagination
    queryset = Expense.objects.all()
    filterset_fields = ('date',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ExpenseSerializer
        else:
            return ExpenseCreateUpdateSerializer
