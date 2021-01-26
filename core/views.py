from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, renderers
from rest_framework.decorators import action
from rest_framework.response import Response

from .permissions import IsAdminOrOwnerOrReadOnly

from .models import Offer, Favorites
from .serializers import UserSerializer, OfferSerializer, FavoritesSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def exists(self, request, *args, **kwargs):
        return Response(self.queryset.filter(pk=self.get_object().pk).exists())

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def exists(self, request, *args, **kwargs):
        return Response(self.queryset.filter(pk=self.get_object().pk).exists())

class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [IsAdminOrOwnerOrReadOnly]
