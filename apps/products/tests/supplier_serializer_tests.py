from rest_framework import test

from ..models import Supplier
from ..serializers import SupplierSerializer


class SupplierSerializerTests(test.APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.fields = ('id', 'name', 'address', 'phone')

        cls.test_data = {
            'name': 'TestCia',
            'address': 'TestStreet',
            'phone': '99999999999'
        }

        cls.update_test_data = {
            'name': 'NewTestCia',
            'address': 'NewTestStreet',
            'phone': '99988888888'
        }

    @staticmethod
    def __create_a_supplier(supplier_data):
        serializer: SupplierSerializer = SupplierSerializer(data=supplier_data)
        serializer.is_valid()

        instance: Supplier = serializer.save()

        return instance

    def test_if_supplier_serializer_have_all_fields(self):
        """
        Tests if supplier serializer have all fields (id, name, address and phone)
        """

        serializer: SupplierSerializer = SupplierSerializer()

        for field in serializer.fields:
            self.assertIn(field, self.fields)

    def test_if_supplier_serializer_is_creating_a_supplier(self):
        """
        Tests if supplier serializer is creating a supplier instance and retrieving it
        """

        serializer: SupplierSerializer = SupplierSerializer(data=self.test_data)
        serializer.is_valid()

        instance: Supplier = serializer.save()

        created: Supplier = Supplier.objects.get(pk=instance.id)

        self.assertIsNotNone(created)

        self.assertEqual(created.name, self.test_data.get('name'))
        self.assertEqual(created.address, self.test_data.get('address'))
        self.assertEqual(created.phone, self.test_data.get('phone'))

    def test_if_supplier_serializer_is_updating_a_supplier_instance(self):
        """
        Tests if supplier serializer can update a supplier instance
        """

        created: Supplier = self.__create_a_supplier(self.test_data)
        serializer: SupplierSerializer = SupplierSerializer()

        serializer.update(created, self.update_test_data)

        updated: Supplier = Supplier.objects.get(pk=created.id)

        self.assertEqual(updated.name, self.update_test_data.get('name'))
        self.assertEqual(updated.address, self.update_test_data.get('address'))
        self.assertEqual(updated.phone, self.update_test_data.get('phone'))

    def test_if_supplier_serializer_returns_the_correct_json(self):

        created: Supplier = self.__create_a_supplier(self.test_data)

        json = self.test_data.copy()
        json['id'] = created.id

        serializer: SupplierSerializer = SupplierSerializer(instance=created)

        self.assertDictEqual(json, serializer.data)
