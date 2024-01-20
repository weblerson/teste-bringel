from rest_framework import test

from ..serializers import PriceHistorySerializer
from ..models import PriceHistory, Product, Supplier


class PriceHistorySerializerTests(test.APITestCase):

    @classmethod
    def setUpTestData(cls):
        test_supplier_data = {
            'name': 'TestCia',
            'address': 'TestStreet',
            'phone': '99999999999'
        }

        cls.fields = ('id', 'product', 'price', 'start', 'end')

        supplier: Supplier = Supplier.objects.create(**test_supplier_data)

        test_product_data = {
            'name': 'Test Science Product',
            'description': 'Test Description',
            'category': 1,
            'supplier': supplier
        }

        product: Product = Product.objects.create(**test_product_data)

        cls.test_data = {
            'product': product.id,
            'price': 10,
        }

        cls.new_history_test_data = {
            'product': product.id,
            'price': 15
        }

    @staticmethod
    def __create_price_history_instance(price_history_data):
        serializer: PriceHistorySerializer = PriceHistorySerializer(data=price_history_data)

        serializer.is_valid()
        instance: PriceHistory = serializer.save()

        return instance

    def test_if_price_history_serializer_have_all_fields(self):
        """
        Tests if price history serializer have all fields (id, product, price, start and end)
        """
        serializer: PriceHistorySerializer = PriceHistorySerializer()

        for field in self.fields:
            self.assertIn(field, serializer.fields)

    def test_if_price_history_serializer_is_creating_a_price_history(self):
        """
        Tests if price history serializer is creating a new price history instance
        """
        serializer: PriceHistorySerializer = PriceHistorySerializer(data=self.test_data)

        serializer.is_valid()
        instance: PriceHistory = serializer.save()

        created: PriceHistory = PriceHistory.objects.get(pk=instance.id)

        self.assertIsNotNone(created)

        self.assertEqual(created.product.id, self.test_data.get('product'))
        self.assertEqual(created.price, self.test_data.get('price'))
        self.assertEqual(created.start, instance.start)
        self.assertIsNone(created.end)

    def test_if_when_a_new_price_history_is_created_it_changes_the_last_history_end_date(self):
        """
        Tests if when a new price history is created it changed the last history end date to it's start date
        """

        self.__create_price_history_instance(self.test_data)
        instance: PriceHistory = self.__create_price_history_instance(self.new_history_test_data)

        last: PriceHistory = PriceHistory.objects.filter(product=instance.product).order_by('start').first()

        self.assertIsNotNone(last.end)
        self.assertEqual(last.end, instance.start)

    def test_if_price_history_serializer_returns_the_correct_json(self):
        """
        Tests if price history serializer returns the correct JSON
        """

        instance: PriceHistory = self.__create_price_history_instance(self.test_data)
        serializer: PriceHistorySerializer = PriceHistorySerializer(instance=instance)

        expected_json = {
            'id': instance.id,
            'product': instance.product.id,
            'price': instance.price,
            'start': instance.start.strftime('%Y-%m-%d'),
            'end': instance.end
        }

        self.assertDictEqual(expected_json, serializer.data)
