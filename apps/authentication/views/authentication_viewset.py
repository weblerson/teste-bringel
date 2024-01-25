from rest_framework import viewsets

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import serializers

from rest_framework.decorators import action

from rest_framework_simplejwt.tokens import RefreshToken

from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication

from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer


@extend_schema_view(
    generate_jwt_token_for_customer=extend_schema(
        responses={
            status.HTTP_200_OK: inline_serializer(
                name='InlineJwtTokenSerializer',
                fields={
                    'access': serializers.CharField(default='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxNCIsIm5h'
                                                            'bWUiOiJsZXJzaW5obyBkYSBzaWx2YSBhbWlndXJ1bWkiLCJpYXQiOjE1MT'
                                                            'YyMzkwMjJ9.nC09Da53OMLQdIOrbkeYNTpyYVDaZlbAjyBC7rN2M3E'),

                    'refresh': serializers.CharField(default='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxNCIsIm5h'
                                                             'bWUiOiJuaW5hIGRhIHNpbHZhIGFtaWd1cnVtaSIsImlhdCI6MTUxNjIzO'
                                                             'TAyMn0.race4dBfOvg3L_1AdoK8ewUYEqkq_2ZwzXvhoU5LO-M')
                }
            )
        }
    )
)
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

    def get_permissions(self):
        match self.action:
            case 'generate_jwt_token_for_customer':
                permission_classes = [permissions.IsAuthenticated]

            case _:
                permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]
