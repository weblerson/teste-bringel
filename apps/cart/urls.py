from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

router: DefaultRouter = DefaultRouter()
router.register(r'carts', views.CartViewSet, basename='cart')


urlpatterns = [
    path('', include(router.urls))
]
