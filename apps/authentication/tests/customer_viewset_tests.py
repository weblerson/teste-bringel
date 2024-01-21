from rest_framework import test
from rest_framework.test import APIClient

from rest_framework import status

from rest_framework.reverse import reverse

from django.utils import timezone

from oauth2_provider.models import Application, AccessToken

from ..models import Customer
from ..serializers import CustomerSerializer


class CustomerViewSetTests(test.APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client: APIClient = APIClient()

        cls.list_url = reverse('customer-list')
        cls.detail_url = reverse('customer-detail', args=[1])

        cls.oauth_url = '/api/o/token/'
        cls.jwt_url = reverse('token_obtain_pair')

        login_data = {
            'username': 'admin',
            'email': 'admin@admin.dev',
            'password': 'admin'
        }
        serializer: CustomerSerializer = CustomerSerializer(data=login_data)
        serializer.is_valid()

        admin: Customer = serializer.create(serializer.validated_data)
        cls.admin = admin

        cls.customer_data = {
            'username': 'testuser',
            'email': 'test@test.dev',
            'password': 'testpassword'
        }

        cls.update_data = {
            'username': 'updatedtestuser',
            'email': 'updatedtest@test.dev'
        }

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

    def __get_jwt_access_token(self, oauth_access_token: str):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {oauth_access_token}')
        jwt_response = self.client.get(self.jwt_url)
        jwt_access_token = jwt_response.data.get('access')

        return jwt_access_token

    def __authenticate(self):
        oauth = self.__get_oauth_access_token(self.admin)
        jwt = self.__get_jwt_access_token(oauth)
        self.client.credentials(HTTP_AUTHORIZATION=self.__create_authorization_header(jwt))

    def test_if_viewset_permissions_are_correct(self):
        """
        Tests if ViewSet permissions are correct (create: Any; the rest: Authentication needed)
        """

        list_response = self.client.get(self.list_url)
        retrieve_response = self.client.get(self.detail_url)
        create_response = self.client.post(self.list_url, data=self.customer_data)
        update_response = self.client.patch(self.detail_url, data=self.update_data)
        delete_response = self.client.delete(self.detail_url)

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(update_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(delete_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_if_viewset_protected_urls_can_only_be_accessed_with_a_jwt_token(self):
        """
        Tests igf ViewSet actions can only be accessed with a JWT token instead of an OAuth access token
        """

        oauth = self.__get_oauth_access_token(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=self.__create_authorization_header(oauth))

        update_response = self.client.patch(self.detail_url, data=self.update_data)
        delete_response = self.client.delete(self.detail_url)

        self.assertEqual(update_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(delete_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_if_list_is_paginated(self):
        """
        Tests if ViewSet list action is returning a paginated JSON
        """

        self.__authenticate()

        response = self.client.get(self.list_url)

        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_create_is_creating_new_customers(self):
        """
        Tests if ViewSet create action is creating new users
        """

        response = self.client.post(self.list_url, data=self.customer_data)

        customer: Customer = Customer.objects.get(pk=response.data.get('id'))

        self.assertIsNotNone(customer)

        self.assertEqual(customer.get_username(), self.customer_data.get('username'))
        self.assertEqual(customer.email, self.customer_data.get('email'))
        self.assertTrue(customer.check_password(self.customer_data.get('password')))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_if_update_is_updating_customer_data(self):
        """
        Tests if ViewSet update action is updating an existing customer data
        """

        self.__authenticate()

        self.client.post(self.list_url, data=self.customer_data)
        response = self.client.patch(self.detail_url, data=self.update_data)

        customer: Customer = Customer.objects.get(pk=response.data.get('id'))

        self.assertIsNotNone(customer)

        self.assertEqual(customer.get_username(), self.update_data.get('username'))
        self.assertEqual(customer.email, self.update_data.get('email'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_id_destroy_is_deleting_an_existing_customer(self):
        """
        Tests if ViewSet destroy action is deleting an existing user
        """

        self.__authenticate()

        create_response = self.client.post(self.list_url, data=self.customer_data)
        delete_response = self.client.delete(self.detail_url)

        from time import sleep

        sleep(1)
        customer = Customer.objects.filter(pk=create_response.get('id'))

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(customer.exists())
