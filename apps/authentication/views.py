from rest_framework import viewsets
from rest_framework import permissions

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import action

from rest_framework_simplejwt.tokens import RefreshToken

from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication

from .models import Customer
from .serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def destroy(self, request, *args, **kwargs):
        """
        A customer cannot remove an account that is not theirs
        """
        customer: Customer = self.get_object()
        if request.user != customer:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)

    def get_permissions(self):
        match self.action:
            case 'create':
                permission_classes = [permissions.AllowAny]

            case _:
                permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]


class AuthenticationViewSet(viewsets.ViewSet):

    authentication_classes = [OAuth2Authentication]

    @staticmethod
    @action(detail=False, url_path='')
    def generate_jwt_token_for_customer(request: Request):
        refresh = RefreshToken.for_user(request.user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_200_OK)
