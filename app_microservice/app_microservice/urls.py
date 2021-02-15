from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from core import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'offers', views.OfferViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),

    # Util
    path('subscribers/', views.SubscribersView.as_view()),
    path('species/', views.SpeciesView.as_view()),

    # Auth
    path(
        'api-auth/',
        include('rest_framework.urls', namespace='rest_framework')
    ),
    path(
        'api/token/google',
        views.GoogleIdTokenLoginView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'
    ),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Admin
    path('internal/admin', admin.site.urls),
    path("internal/docs/", include("app_microservice.docs_urls")),
]

# For local development convenience, serve static content directly from the
# django wsgi or devserver process.
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns(prefix='/static')
