from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .models import Asset, AssetClass, Exchange
from .serializers import (AssetClassSerializer, AssetSerializer,
                          ExchangeSerializer)


class AssetView(viewsets.ModelViewSet):

    def get_queryset(self, *args, **kwargs):
        return Asset.objects.all()

    def get_serializer_class(self):
        return AssetSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that the user view
        requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class AssetClassView(viewsets.ModelViewSet):

    def get_queryset(self, *args, **kwargs):
        return AssetClass.objects.all()

    def get_serializer_class(self):
        return AssetClassSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that the user view
        requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class ExchangeView(viewsets.ModelViewSet):

    def get_queryset(self, *args, **kwargs):
        return Exchange.objects.all()

    def get_serializer_class(self):
        return ExchangeSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that the user view
        requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]