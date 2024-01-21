from rest_framework import test
from rest_framework.test import APIClient

from rest_framework.reverse import reverse

from rest_framework import status

from django.utils import timezone

from authentication.serializers import CustomerSerializer
from authentication.models import Customer
from ..models import Product, Supplier

from ..serializers import ProductSerializer

from oauth2_provider.models import Application, AccessToken
from rest_framework_simplejwt.tokens import RefreshToken


class ProductViewSetTests(test.APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client: APIClient = APIClient()

        cls.list_url = reverse('product-list')
        cls.detail_url = reverse('product-detail', args=[1])

        cls.customer_data = {
            'username': 'testuser',
            'email': 'test@test.dev',
            'password': 'testpassword'
        }

        test_supplier_data = {
            'name': 'TestCia',
            'address': 'TestStreet',
            'phone': '99999999999'
        }
        supplier: Supplier = Supplier.objects.create(**test_supplier_data)

        default_product_data = {
            'name': 'Test Product',
            'description': 'Test description',
            'category': Product.Category.SCIENCE,
            'supplier': supplier.id
        }
        serializer: ProductSerializer = ProductSerializer(data=default_product_data)
        serializer.is_valid()

        cls.product: Product = serializer.save()

        cls.product_data = {
            'name': 'Product X',
            'description': 'Test description',
            'category': Product.Category.SCIENCE,
            'supplier': supplier.id
        }

        cls.update_product_data = {
            'name': 'Updated Test Product',
            'description': 'Updated test description'
        }

        cls.expected_sku = 'TC1-PX'

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

        update_serializer: ProductSerializer = ProductSerializer()

        customer: Customer = serializer.create(serializer.validated_data)
        customer = update_serializer.update(customer, {'is_staff': True})

        return customer

    def test_if_viewset_permission_are_correct(self):
        """
        Tests if product view set are correct (list and retrieve: Any; the rest: Admin needed)
        """

        list_response = self.client.get(self.list_url)
        retrieve_response = self.client.get(self.detail_url)
        create_response = self.client.post(self.list_url, data=self.product_data)
        update_response = self.client.patch(self.detail_url, data=self.update_product_data)
        delete_response = self.client.delete(self.detail_url)

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertEqual(create_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(update_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(delete_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tests_ig_viewset_protected_urls_cannot_be_accessed_with_a_non_admin_jwt_token(self):
        """
        Tests if product view set action cannot be accessed with a common user JWT token
        """

        customer: Customer = self.__get_customer(self.customer_data)
        jwt, _ = self.__get_jwt_pair(customer)
        self.client.credentials(HTTP_AUTHORIZATION=self.__create_authorization_header(jwt))

        create_response = self.client.post(self.list_url, data=self.product_data)
        update_response = self.client.patch(self.detail_url, data=self.update_product_data)
        delete_response = self.client.delete(self.detail_url)

        self.assertEqual(create_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(update_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_if_viewset_protected_urls_can_only_be_accessed_with_a_jwt_admin_token(self):
        """
        Tests if product view set actions can only be accessed with a JWT token of an admin
         instead of an OAuth access token
        """

        customer: Customer = self.__get_admin_customer(self.customer_data)
        oauth = self.__get_oauth_access_token(customer)
        jwt, _ = self.__get_jwt_pair(customer)
        self.client.credentials(HTTP_AUTHORIZATION=self.__create_authorization_header(oauth))

        create_response = self.client.post(self.list_url, data=self.product_data)
        update_response = self.client.patch(self.detail_url, data=self.update_product_data)
        delete_response = self.client.delete(self.detail_url)

        self.assertEqual(create_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(update_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(delete_response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=self.__create_authorization_header(jwt))

        create_response = self.client.post(self.list_url, data=self.product_data)
        update_response = self.client.patch(self.detail_url, data=self.update_product_data)
        delete_response = self.client.delete(self.detail_url)

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_if_list_is_paginated(self):
        """
        Tests if product view set list action is returning a paginated JSON
        """

        customer: Customer = self.__get_admin_customer(self.customer_data)
        self.__authenticate(customer)

        response = self.client.get(self.list_url)

        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_create_is_creating_new_product(self):
        """
        Tests if product view set create action is creating new products
        """

        customer: Customer = self.__get_admin_customer(self.customer_data)
        self.__authenticate(customer)

        response = self.client.post(self.list_url, data=self.product_data)

        product: Product = Product.objects.get(pk=response.data.get('id'))

        self.assertIsNotNone(product)

        self.assertEqual(product.name, self.product_data.get('name'))
        self.assertEqual(product.description, self.product_data.get('description'))
        self.assertEqual(product.category, self.product_data.get('category'))
        self.assertEqual(product.sku, self.expected_sku)
        self.assertEqual(product.average_review, 0.0)
        self.assertEqual(product.supplier.id, self.product_data.get('supplier'))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_if_update_is_updating_product_data(self):
        """
        Tests if product view set update action is updating an existing product data
        """

        customer: Customer = self.__get_admin_customer(self.customer_data)
        self.__authenticate(customer)

        self.client.post(self.list_url, data=self.product_data)
        response = self.client.patch(self.detail_url, data=self.update_product_data)

        product: Product = Product.objects.get(pk=response.data.get('id'))

        self.assertIsNotNone(product)

        self.assertEqual(product.name, self.update_product_data.get('name'))
        self.assertEqual(product.description, self.update_product_data.get('description'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_id_destroy_is_deleting_an_existing_product(self):
        """
        Tests if product view set destroy action is deleting an existing product
        """

        customer: Customer = self.__get_admin_customer(self.customer_data)
        self.__authenticate(customer)

        create_response = self.client.post(self.list_url, data=self.product_data)
        delete_response = self.client.delete(self.detail_url)

        from time import sleep

        sleep(1)
        product = Product.objects.filter(pk=create_response.get('id'))

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(product.exists())
