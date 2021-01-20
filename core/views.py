from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions

from .permissions import IsOwnerOrReadOnly

from .models import Offer, Favorites
from .serializers import UserSerializer, GroupSerializer, OfferSerializer, FavoritesSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]#, IsOwnerOrReadOnly]

class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]#, IsOwnerOrReadOnly]
