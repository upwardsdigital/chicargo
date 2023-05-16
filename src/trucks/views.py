from rest_framework import generics, permissions
from .serializers import TruckSerializer, TruckCreateSerializer
from .models import Truck
from .filters import TruckFilter


class TruckListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Truck.objects.all().order_by('-id')
    filterset_class = TruckFilter

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TruckCreateSerializer
        else:
            return TruckSerializer
