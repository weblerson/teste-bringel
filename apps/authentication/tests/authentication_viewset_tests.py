from rest_framework import test
from rest_framework.test import APIClient

from rest_framework import status

from rest_framework.reverse import reverse

from django.utils import timezone

from oauth2_provider.models import Application, AccessToken

from ..models import Customer
from ..serializers import CustomerSerializer


class AuthenticationViewSetTests(test.APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client: APIClient = APIClient()

        cls.token_url = reverse('token_obtain_pair')

        login_data = {
            'username': 'admin',
            'email': 'admin@admin.dev',
            'password': 'admin'
        }
        serializer: CustomerSerializer = CustomerSerializer(data=login_data)
        serializer.is_valid()

        admin: Customer = serializer.create(serializer.validated_data)
        cls.admin = admin

    @staticmethod
    def __create_authorization_header(token: str):
        return f'Bearer {token}'

    @staticmethod
    def __get_oauth_access_token(admin: Customer):
        application: Application = Application.objects.create(
            name='Test Client',
            redirect_uris='',
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            user=admin
        )

        access_token = AccessToken.objects.create(
            user=admin,
            scope='read write',
            expires=timezone.now() + timezone.timedelta(seconds=300),
            token='secret-access-token-key',
            application=application
        )

        return access_token

    def test_if_generate_token_for_customer_only_can_be_accessed_with_an_oauth_access_token(self):
        """
        Tests if 'generate_jwt_token_for_customer' action only can be accessed with an OAuth access token in header
        """

        response = self.client.get(self.token_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_if_generate_jwt_token_for_customer_retrieves_the_token_pair(self):
        """
        Tests if 'generate_jwt_token_for_customer' action retrieves the token pair - access and refresh
        """

        oauth = self.__get_oauth_access_token(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=self.__create_authorization_header(oauth))

        response = self.client.get(self.token_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
