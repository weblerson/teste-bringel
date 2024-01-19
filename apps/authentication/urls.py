from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import TokenRefreshView

from . import views

router = DefaultRouter()
router.register(r'customers', views.CustomerViewSet, basename='customer')

urlpatterns = [
    path('', include(router.urls)),

    path(
        'token/',
        views.AuthenticationViewSet.as_view({'get': 'generate_jwt_token_for_customer'}),
        name='generate_jwt_token_for_customer'
    ),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
