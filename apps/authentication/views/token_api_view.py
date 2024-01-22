from drf_spectacular.utils import extend_schema, inline_serializer
from oauth2_provider.views import TokenView

from rest_framework import serializers
from rest_framework import views


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
        )
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
