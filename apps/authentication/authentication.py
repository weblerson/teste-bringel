from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken


class JWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        auth_header = self.get_header(request)

        if not auth_header:
            return None

        try:
            raw_token = self.get_raw_token(auth_header)
            untyped_token: UntypedToken = UntypedToken(raw_token)
            untyped_token.verify()

            return super().authenticate(request)

        except (InvalidToken, TokenError):
            return None
