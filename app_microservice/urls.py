from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from core import views

router = routers.DefaultRouter()
router.register(r'user', views.AuthViewSet, basename='user')
router.register(r'users', views.UserViewSet)
router.register(r'offers', views.OfferViewSet)
router.register(r'favorites', views.FavoritesViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

#urlpatterns = format_suffix_patterns(urlpatterns)
