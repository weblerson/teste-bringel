from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import TokenRefreshView

from . import views

router = DefaultRouter()
router.register(r'customers', views.CustomerViewSet, basename='customer')

urlpatterns = [
    path('', include(router.urls)),

    # OAuth
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # JWT
    path(
        'token/',
        views.AuthenticationViewSet.as_view({'get': 'generate_jwt_token_for_customer'}),
        name='token_obtain_pair'
    ),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
