from rest_framework import viewsets

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import action

from rest_framework_simplejwt.tokens import RefreshToken

from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication


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
