from rest_framework import test

from ..models import Product, Supplier
from ..serializers import ProductSerializer


class ProductSerializerTests(test.APITestCase):

    @classmethod
    def setUpTestData(cls):
        test_supplier_data = {
            'name': 'TestCia',
            'address': 'TestStreet',
            'phone': '99999999999'
        }

        cls.fields = (
            'id',
            'name',
            'description',
            'sku',
            'category',
            'average_review',
            'customers',
            'supplier'
        )

        supplier: Supplier = Supplier.objects.create(**test_supplier_data)
        cls.supplier = supplier

        test_data = {
            'name': 'Test Science Product',
            'description': 'Test Description',
            'category': 1,
            'supplier': supplier.id
        }
        cls.test_data = test_data

        cls.expected_sku = 'TC1-TSP'

    @staticmethod
    def __create_supplier(supplier_data):
        supplier: Supplier = Supplier.objects.create(**supplier_data)

        return supplier

    def test_if_product_serializer_have_all_fields(self):
        """
        Tests if product serializer have all fields: (
            id, name, description, sku, category, average review, customers and supplier
        )
        """

        serializer: ProductSerializer = ProductSerializer()

        for field in serializer.fields:
            self.assertIn(field, self.fields)

    def test_if_product_serializer_is_creating_a_product(self):
        """
        Tests if product serializer is creating a new customer instance and retrieving it
        """

        serializer: ProductSerializer = ProductSerializer(data=self.test_data)

        self.assertTrue(serializer.is_valid())
        product_instance: Product = serializer.save()

        created: Product = Product.objects.get(pk=product_instance.id)

        self.assertIsNotNone(created)

        self.assertEqual(created.name, self.test_data.get('name'))
        self.assertEqual(created.description, self.test_data.get('description'))
        self.assertEqual(created.category, self.test_data.get('category'))
        self.assertEqual(created.supplier.id, self.test_data.get('supplier'))

    def test_if_supplier_attribute_goes_null_when_the_related_supplier_is_deleted(self):
        """
        Tests if supplier attribute goes null when the product's related supplier is deleted
        """

        supplier_data = {
            'name': 'NewCia',
            'address': 'NewStreet',
            'phone': '99999999998'
        }
        supplier: Supplier = self.__create_supplier(supplier_data)

        test_data = self.test_data.copy()
        test_data['supplier'] = supplier.id

        serializer: ProductSerializer = ProductSerializer(data=self.test_data)
        serializer.is_valid()

        product_instance: Product = serializer.save()
        Supplier.objects.get(pk=product_instance.supplier.id).delete()

        created: Product = Product.objects.get(pk=product_instance.id)
        self.assertIsNone(created.supplier)

    def test_if_sku_is_being_generated_correctly(self):
        """
        Tests if the sku field is being generated correctly
        """

        serializer: ProductSerializer = ProductSerializer(data=self.test_data)

        serializer.is_valid()
        product_instance: Product = serializer.save()

        created: Product = Product.objects.get(pk=product_instance.id)

        self.assertEqual(created.sku, self.expected_sku)

    def test_if_product_serializer_is_updating_average_review(self):
        """
        Tests if product serializer is updating the product's average review automatically
        """

        ...
