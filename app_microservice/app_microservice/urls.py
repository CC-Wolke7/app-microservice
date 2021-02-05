from django.conf import settings
from django.conf.urls import url
from django.urls import include, path

from rest_framework import routers

from core import views

router = routers.DefaultRouter()
router.register(r'users', views.WSUserViewSet)
router.register(r'offers', views.OfferViewSet)
router.register(r'favorites', views.FavoritesViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('images/', views.Images.as_view()),
    path('', include('social_django.urls', namespace='social')),
    path(
        'api-auth/',
        include('rest_framework.urls', namespace='rest_framework')
    )
]

# For local development convenience, serve static content directly from the
# django wsgi or devserver process.
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns(prefix='/static')
