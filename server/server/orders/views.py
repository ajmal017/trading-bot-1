from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Order
from .serializers import OrderCreateSerializer, OrderSerializer


class OrderView(viewsets.ModelViewSet):

    def get_queryset(self, *args, **kwargs):
        return Order.objects.all()

    def get_serializer_class(self):
        """
        Instantiates and returns the serializer that the order view requires.
        """
        if self.action in ['list', 'retrieve']:
            print('\nOrderSerializer')
            return OrderSerializer
        print('\nOrderCreateSerializer')
        return OrderCreateSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that the order view
        requires.
        """
        if self.action == 'delete':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]