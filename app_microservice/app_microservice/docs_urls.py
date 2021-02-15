from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from django.urls import path

# Configuration for API documentation
schema_view = get_schema_view(
    openapi.Info(title='App Microservice', default_version='v1'),
    public=True,
)

urlpatterns = [
    path('', schema_view.with_ui('redoc'), name='schema-redoc'),
    path('swagger/', schema_view.with_ui('swagger'), name='schema-swagger-ui'),
    path(
        'swagger.json',
        schema_view.without_ui(),
        kwargs={'format': '.json'},
        name='schema-json'
    ),
]
