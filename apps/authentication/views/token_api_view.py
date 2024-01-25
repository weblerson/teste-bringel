from drf_spectacular.utils import extend_schema, inline_serializer
from oauth2_provider.views import TokenView

from rest_framework import serializers
from rest_framework import views
from rest_framework import status


class TokenApiView(TokenView, views.APIView):
    @extend_schema(
        request=inline_serializer(
            name="InlineTokenSerializer",
            fields={
                "username": serializers.CharField(),
                "password": serializers.CharField(),
                "grant_type": serializers.CharField(required=False),
                "client_secret": serializers.CharField(),
                "client_id": serializers.CharField(),
            },
        ),
        responses={
            status.HTTP_200_OK: inline_serializer(
                name='InlineResponseTokenSerializer',
                fields={
                    'access_token': serializers.CharField(default='lSUruikOljhghYBNjasd85P8Yubgh9'),
                    'expires_in': serializers.IntegerField(default=36000),
                    'token_type': serializers.CharField(default='Bearer'),
                    'scope': serializers.CharField(default='read write groups'),
                    'refresh_token': serializers.CharField(default='jsuTGb56Tgak8pTkshgf5olYncjsuo')
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
