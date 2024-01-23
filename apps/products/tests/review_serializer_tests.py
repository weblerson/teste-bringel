from rest_framework import test

from ..models import Review, Supplier, Product
from authentication.models import Customer

from unittest.mock import patch

from ..serializers import ReviewSerializer
from ..tasks import update_product_average_review


class ReviewSerializerTests(test.APITestCase):

    @classmethod
    def setUpTestData(cls):
        test_supplier_data = {
            'name': 'TestCia',
            'address': 'TestStreet',
            'phone': '99999999999'
        }

        cls.fields = ('product', 'customer', 'value')

        supplier: Supplier = Supplier.objects.create(**test_supplier_data)

        test_product_data = {
            'name': 'Test Science Product',
            'description': 'Test Description',
            'category': 1,
            'supplier': supplier
        }

        product: Product = Product.objects.create(**test_product_data)

        test_customer_data = {
            'username': 'testuser',
            'email': 'test@test.dev',
            'password': 'testpassword'
        }

        customer: Customer = Customer.objects.create(**test_customer_data)

        cls.test_data = {
            'product': product.id,
            'customer': customer.id,
            'value': 4.5
        }

        cls.new_review_test_data = {
            'product': product.id,
            'customer': customer.id,
            'value': 3.0
        }

        cls.update_test_data = {
            'value': 5.0
        }

    @staticmethod
    def __create_review_instance(review_data):
        serializer: ReviewSerializer = ReviewSerializer(data=review_data)
        serializer.is_valid()

        instance: Review = serializer.save()

        return instance

    def test_if_review_serializer_have_all_fields(self):
        """
        Tests if review serializer have all fields (product, customer and value)
        """

        serializer: ReviewSerializer = ReviewSerializer()

        for field in self.fields:
            self.assertIn(field, serializer.fields)

    def test_if_review_serializer_can_create_a_review(self):
        """
        Tests if review serializer can create a review
        """

        serializer: ReviewSerializer = ReviewSerializer(data=self.test_data)
        serializer.is_valid()

        instance: Review = serializer.save()

        created = Review.objects.filter(product=instance.product.id).filter(customer=instance.customer.id)

        self.assertTrue(created.exists())
        self.assertEqual(created.first().value, self.test_data.get('value'))

    def test_if_review_serializer_can_update_a_review_value(self):
        """
        Tests if review serializer can update a review's value
        """

        instance: Review = self.__create_review_instance(self.test_data)
        serializer: ReviewSerializer = ReviewSerializer()
        serializer.update(instance, self.update_test_data)

        updated: Review = Review.objects.get(product=instance.product, customer=instance.customer)

        self.assertEqual(updated.value, self.update_test_data.get('value'))

    def test_if_review_serializer_returns_the_correct_json(self):
        """
        Tests if review serializer returns the correct JSON
        """

        instance: Review = self.__create_review_instance(self.test_data)

        expected_json = {
            'product': instance.product.id,
            'customer': instance.customer.id,
            'value': instance.value
        }

        serializer: ReviewSerializer = ReviewSerializer(instance=instance)

        self.assertDictEqual(expected_json, serializer.data)

    @patch('products.tasks.serializers.ProductSerializer.update')
    def test_if_the_average_review_changes_automatically_when_another_review_instance_is_created(
            self,
            serializer_update
    ):
        """
        Tests if the average review of a product changes automatically when another review instance is created
        """

        first_review: Review = self.__create_review_instance(self.test_data)
        product: Product = Product.objects.get(pk=first_review.product.id)

        update_product_average_review(product.id)

        serializer_update.assert_called_with(product, {'average_review': self.test_data.get('value')})

        self.__create_review_instance(self.new_review_test_data)
        Product.objects.get(pk=first_review.product.id)

        average = (self.test_data.get('value') + self.new_review_test_data.get('value')) / 2

        update_product_average_review(first_review.product.id)
        serializer_update.assert_called_with(product, {'average_review': average})
