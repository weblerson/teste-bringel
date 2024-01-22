from rest_framework import test
from rest_framework.test import APIClient

from rest_framework.reverse import reverse

from ..models import Product, Supplier
from ..serializers import ProductSerializer


class RecommendationAlgorithmViewSetTests(test.APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client: APIClient = APIClient()

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

        cls.first_product = {
            'name': 'first science product',
            'description': 'Test description',
            'category': Product.Category.SCIENCE,
            'supplier': supplier.id
        }

        cls.second_product = {
            'name': 'second science product',
            'description': 'Test description',
            'category': Product.Category.SCIENCE,
            'supplier': supplier.id
        }

        cls.third_product = {
            'name': 'fiction product',
            'description': 'Test description',
            'category': Product.Category.FICTION,
            'supplier': supplier.id
        }

        cls.fourth_product = {
            'name': 'didactic product',
            'description': 'Test description',
            'category': Product.Category.DIDACTIC,
            'supplier': supplier.id
        }

    @staticmethod
    def __generate_product(product_data):
        serializer: ProductSerializer = ProductSerializer(data=product_data)
        serializer.is_valid()

        instance: Product = serializer.save()

        return instance

    def test_if_recommendation_algorithm_recommends_the_second_science_product_except_the_first(self):
        """
        Tests if recommendation algorithm recommends the second science product except the first (the main product)
        """

        main_product: Product = self.__generate_product(self.first_product)
        second: Product = self.__generate_product(self.second_product)
        url = reverse('related_products', args=[main_product.id])

        response = self.client.get(url)

        self.assertIn('products', response.data)
        self.assertEqual(len(response.data.get('products')), 1)
        self.assertNotEqual(response.data.get('products')[0].get('id'), main_product.id)
        self.assertEqual(response.data.get('products')[0].get('id'), second.id)

    def test_if_recommendation_algorithm_returns_an_empty_list_when_there_is_only_one_product(self):
        """
        Tests if recommendation algorithm returns an empty list when there is
        only one product with a determined category
        """

        main_product: Product = self.__generate_product(self.third_product)
        url = reverse('related_products', args=[main_product.id])

        response = self.client.get(url)

        self.assertIn('products', response.data)
        self.assertEqual(len(response.data.get('products')), 0)
