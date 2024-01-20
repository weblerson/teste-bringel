from rest_framework import test

from ..models import Supplier, Tag, Product
from ..serializers import TagSerializer


class SupplierSerializerTests(test.APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.fields = ('name', 'product')

        test_supplier_data = {
            'name': 'TestCia',
            'address': 'TestStreet',
            'phone': '99999999999'
        }
        supplier: Supplier = Supplier.objects.create(**test_supplier_data)

        test_product_data = {
            'name': 'Test Science Product',
            'description': 'Test Description',
            'category': 1,
            'supplier': supplier.id
        }
        product: Product = Product.objects.create(**test_product_data)

        cls.test_data = {
            'name': 'book',
            'product': product.id
        }

    def test_if_tag_serializer_have_all_fields(self):
        """
        Tests if tag serializer have all fields (name and product)
        """

        serializer: TagSerializer = TagSerializer()

        for field in serializer.fields:
            self.assertIn(field, self.fields)

    def test_if_tag_serializer_is_creating_a_tag(self):
        """
        Tests if tag serializer is creating a tag instance and retrieving it
        """

        serializer: TagSerializer = TagSerializer(data=self.test_data)
        serializer.is_valid()

        instance: Tag = serializer.save()

        created: Tag = Tag.objects.get(pk=instance.name)

        self.assertIsNotNone(created)

        self.assertEqual(created.name, self.test_data.get('name'))
        self.assertEqual(created.product.id, self.test_data.get('address'))

    def test_if_tag_serializer_returns_the_correct_json(self):
        """
        Tests if tag serializer returns te correct JSON
        """

        json = self.test_data.copy()

        serializer: TagSerializer = TagSerializer(data=self.test_data)
        serializer.is_valid()

        serializer.save()

        self.assertDictEqual(json, serializer.data)
