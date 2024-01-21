from rest_framework import test
from rest_framework.test import APIClient

from rest_framework.reverse import reverse

from rest_framework import status

from django.utils import timezone

from authentication.models import Customer
from authentication.serializers import CustomerSerializer
from ..models import Tag, Product, Supplier

from ..serializers import SupplierSerializer, ProductSerializer, TagSerializer

from oauth2_provider.models import Application, AccessToken
from rest_framework_simplejwt.tokens import RefreshToken


class TagViewSetTests(test.APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client: APIClient = APIClient()

        cls.list_url = reverse('tag-list')
        cls.detail_url = reverse('tag-detail', args=['test'])

        cls.customer_data = {
            'username': 'testuser',
            'email': 'test@test.dev',
            'password': 'testpassword'
        }

        supplier_data = {
            'name': 'Default TestCia',
            'address': 'Default TestStreet',
            'phone': '99999999999'
        }
        serializer: SupplierSerializer = SupplierSerializer(data=supplier_data)
        serializer.is_valid()

        supplier: Supplier = serializer.save()

        product_data = {
            'name': 'Test Product',
            'description': 'Test description',
            'category': Product.Category.SCIENCE,
            'supplier': supplier.id
        }
        serializer: ProductSerializer = ProductSerializer(data=product_data)
        serializer.is_valid()

        product: Product = serializer.save()
        cls.product = product

        cls.tag_data = {
            'name': 'test',
            'product': product.id
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

    @staticmethod
    def __get_jwt_pair(customer: Customer):
        refresh = RefreshToken.for_user(customer)

        return str(refresh.access_token), str(refresh)

    def __authenticate(self, customer: Customer):
        access, _ = self.__get_jwt_pair(customer)
        self.client.credentials(HTTP_AUTHORIZATION=self.__create_authorization_header(access))

    @staticmethod
    def __get_customer(customer_data):
        serializer: CustomerSerializer = CustomerSerializer(data=customer_data)
        serializer.is_valid()

        customer: Customer = serializer.create(serializer.validated_data)

        return customer

    @staticmethod
    def __get_admin_customer(customer_data):
        serializer: CustomerSerializer = CustomerSerializer(data=customer_data)
        serializer.is_valid()

        update_serializer: CustomerSerializer = CustomerSerializer()

        customer: Customer = serializer.create(serializer.validated_data)
        customer = update_serializer.update(customer, {'is_staff': True})

        return customer

    @staticmethod
    def __get_tag(tag_data):
        serializer: TagSerializer = TagSerializer(data=tag_data)
        serializer.is_valid()

        return serializer.save()

    def test_if_viewset_permission_are_correct(self):
        """
        Tests if tag view set are correct (list: Any; destroy: Admin needed; the rest: Authentication needed)
        """

        list_response = self.client.get(self.list_url)
        create_response = self.client.post(self.list_url, data=self.tag_data)
        delete_response = self.client.delete(self.detail_url)

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(create_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(delete_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tests_if_viewset_protected_urls_cannot_be_accessed_with_a_non_admin_jwt_token(self):
        """
        Tests if tag view set action cannot be accessed with a common user JWT token
        """

        customer: Customer = self.__get_customer(self.customer_data)
        jwt, _ = self.__get_jwt_pair(customer)
        self.client.credentials(HTTP_AUTHORIZATION=self.__create_authorization_header(jwt))

        delete_response = self.client.delete(self.detail_url)

        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_if_viewset_protected_urls_can_only_be_accessed_with_a_jwt_admin_token(self):
        """
        Tests if tag view set actions can only be accessed with a JWT token of an admin
         instead of an OAuth access token
        """

        customer: Customer = self.__get_admin_customer(self.customer_data)
        oauth = self.__get_oauth_access_token(customer)
        jwt, _ = self.__get_jwt_pair(customer)
        self.client.credentials(HTTP_AUTHORIZATION=self.__create_authorization_header(oauth))

        create_response = self.client.post(self.list_url, data=self.tag_data)
        delete_response = self.client.delete(self.detail_url)

        self.assertEqual(create_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(delete_response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=self.__create_authorization_header(jwt))

        create_response = self.client.post(self.list_url, data=self.tag_data)
        delete_response = self.client.delete(self.detail_url)

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_if_list_is_paginated(self):
        """
        Tests if tag view set list action is returning a paginated JSON
        """

        customer: Customer = self.__get_admin_customer(self.customer_data)
        self.__authenticate(customer)

        response = self.client.get(self.list_url)

        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_create_is_creating_new_tag(self):
        """
        Tests if tag view set create action is creating new tags
        """

        customer: Customer = self.__get_customer(self.customer_data)
        self.__authenticate(customer)

        response = self.client.post(self.list_url, data=self.tag_data)

        tag: Tag = Tag.objects.get(pk=response.data.get('name'))

        self.assertIsNotNone(tag)

        self.assertEqual(tag.name, self.tag_data.get('name'))
        self.assertEqual(tag.product.id, self.tag_data.get('product'))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_if_destroy_is_deleting_an_existing_tag(self):
        """
        Tests if tag view set destroy action is deleting an existing tag
        """

        customer: Customer = self.__get_admin_customer(self.customer_data)
        self.__authenticate(customer)

        create_response = self.client.post(self.list_url, data=self.tag_data)
        delete_response = self.client.delete(self.detail_url)

        from time import sleep

        sleep(1)
        tag = Tag.objects.filter(pk=create_response.get('name'))

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(tag.exists())
