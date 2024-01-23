from rest_framework import test
from rest_framework.test import APIClient

from rest_framework.reverse import reverse

from rest_framework import status

from django.utils import timezone

from authentication.models import Customer
from authentication.serializers import CustomerSerializer
from ..models import Supplier, Product, Review

from ..serializers import SupplierSerializer, ProductSerializer, ReviewSerializer

from oauth2_provider.models import Application, AccessToken
from rest_framework_simplejwt.tokens import RefreshToken


class ReviewViewSetTests(test.APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client: APIClient = APIClient()

        cls.list_url = reverse('review-list')
        cls.detail_url = reverse('review-detail', args=[1])

        customer_data = {
            'username': 'testuser',
            'email': 'test@test.dev',
            'password': 'testpassword'
        }
        serializer: CustomerSerializer = CustomerSerializer(data=customer_data)
        serializer.is_valid()

        customer: Customer = serializer.save()
        cls.customer = customer

        test_supplier_data = {
            'name': 'Default TestCia',
            'address': 'Default TestStreet',
            'phone': '99999999999'
        }
        serializer: SupplierSerializer = SupplierSerializer(data=test_supplier_data)
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

        cls.review_data = {
            'product': product.id,
            'customer': customer.id,
            'value': 4.0
        }

        cls.update_review_data = {
            'value': 3.0
        }

        cls.new_review_data = {
            'product': product.id,
            'customer': customer.id,
            'value': 3.5
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
    def __generate_review(review_data):
        serializer: ReviewSerializer = ReviewSerializer(data=review_data)
        serializer.is_valid()

        instance: Review = serializer.save()

        return instance

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

    def test_if_viewset_permission_are_correct(self):
        """
        Tests if review view set are correct (list and retrieve: Any; the rest: Authentication needed)
        """

        list_response = self.client.get(self.list_url)
        create_response = self.client.post(self.list_url, data=self.review_data)
        update_response = self.client.patch(self.detail_url, data=self.review_data)
        delete_response = self.client.delete(self.detail_url)

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(create_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(update_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(delete_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_if_list_is_paginated(self):
        """
        Tests if review view set list action is returning a paginated JSON
        """

        response = self.client.get(self.list_url)

        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_create_is_creating_new_review(self):
        """
        Tests if review view set create action is creating new reviews
        """

        self.__authenticate(self.customer)

        response = self.client.post(self.list_url, data=self.review_data)

        review: Review = Review.objects.filter(customer=response.data.get('customer')).first()

        self.assertIsNotNone(review)

        self.assertEqual(review.product.id, self.review_data.get('product'))
        self.assertEqual(review.customer.id, self.review_data.get('customer'))
        self.assertEqual(review.value, self.review_data.get('value'))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_if_update_is_updating_review_data(self):
        """
        Tests if review view set update action is updating an existing review data
        """

        self.__authenticate(self.customer)

        self.client.post(self.list_url, data=self.review_data)
        response = self.client.patch(self.detail_url, data=self.update_review_data)

        review: Review = Review.objects.filter(customer=response.data.get('customer')).first()

        self.assertIsNotNone(review)

        self.assertEqual(review.value, self.update_review_data.get('value'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_destroy_is_deleting_an_existing_review(self):
        """
        Tests if review view set destroy action is deleting an existing review
        """

        self.__authenticate(self.customer)

        create_response = self.client.post(self.list_url, data=self.review_data)
        delete_response = self.client.delete(self.detail_url)

        from time import sleep

        sleep(1)
        review = Review.objects.filter(customer=create_response.get('customer'))

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(review.exists())
