from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme
from drf_spectacular.contrib.django_oauth_toolkit import DjangoOAuthToolkitScheme
from drf_spectacular.extensions import OpenApiAuthenticationExtension

from authentication import authentication
from oauth2_provider.contrib import rest_framework


class JWTAuthenticationScheme(SimpleJWTScheme):
    target_class = authentication.JWTAuthentication
    name = 'JWTAuthentication'


class OAuth2AuthenticationExtension(OpenApiAuthenticationExtension):
    target_class = 'oauth2_provider.contrib.rest_framework.authentication.OAuth2Authentication'
    name = 'OAuth2Authentication'

    def get_security_requirement(self):
        return [{"OAuth2Authentication": []}]

    def get_security_definition(self):
        return {
            "OAuth2Authentication": {
                "type": "oauth2",
                "flow": "password",
                "tokenUrl": "/api/o/custom/",
                "scopes": {
                    "read": "read scope",
                    "write": "write scope"
                }
            }
        }
