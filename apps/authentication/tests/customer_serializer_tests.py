from rest_framework import test

from ..models import Customer
from ..serializers import CustomerSerializer


class CustomerSerializerTests(test.APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.fields = ('id', 'username', 'email', 'password', 'is_staff')

        cls.test_data = {
            'username': 'testuser',
            'email': 'test@test.dev',
            'password': 'testpassword'
        }

        cls.update_data = {
            'username': 'updatedtestuser',
            'email': 'updatedtest@test.dev'
        }

    def test_if_customer_serializer_have_all_fields(self):
        """
        Tests if customer serializer have all fields: (id, username, email and password)
        """

        serializer: CustomerSerializer = CustomerSerializer()

        for field in serializer.fields:
            self.assertIn(field, self.fields)

    def test_if_customer_serializer_password_field_is_write_only(self):
        """
        Tests if customer serializer's password field is write only - cannot be retrieved
        """

        serializer: CustomerSerializer = CustomerSerializer(data=self.test_data)
        serializer.is_valid()

        self.assertNotIn('password', serializer.data.keys())

    def test_if_customer_serializer_is_validating_customer_username(self):
        """
        Tests if customer serializer is validating his username - it cannot have blank spaces
        """

        test_data = self.test_data.copy()
        test_data['username'] = 'invalid user username'

        serializer: CustomerSerializer = CustomerSerializer(data=test_data)

        self.assertFalse(serializer.is_valid())

    def test_if_customer_serializer_is_validating_customer_email(self):
        """
        Tests if customer serializer is validating his email - must be a valid email address
        """

        test_data = self.test_data.copy()
        test_data['email'] = 'notaemail'

        serializer: CustomerSerializer = CustomerSerializer(data=test_data)

        self.assertFalse(serializer.is_valid())

    def test_is_customer_serializer_is_validating_customer_password(self):
        """
        Tests if customer serializer is validating his password - it cannot have blank spaces
        """

        test_data = self.test_data.copy()
        test_data['password'] = 'invalid user password'

        serializer: CustomerSerializer = CustomerSerializer(data=test_data)

        self.assertFalse(serializer.is_valid())

    def test_if_customer_serializer_is_creating_a_customer(self):
        """
        Tests if customer serializer is creating a new customer instance and retrieving it
        """

        serializer: CustomerSerializer = CustomerSerializer(data=self.test_data)

        self.assertTrue(serializer.is_valid())
        created = serializer.save()

        created = Customer.objects.get(pk=created.id)

        self.assertIsNotNone(created)

        self.assertEqual(created.get_username(), self.test_data.get('username'))
        self.assertEqual(created.email, self.test_data.get('email'))
        self.assertTrue(created.check_password(self.test_data.get('password')))

    def test_if_customer_serializer_is_updating_a_created_customer_data(self):
        """
        Tests if customer serializer is updating a created customer instance's username and email
        """

        serializer: CustomerSerializer = CustomerSerializer(data=self.test_data)

        self.assertTrue(serializer.is_valid())
        created = serializer.save()

        serializer.update(created, self.update_data)

        updated = Customer.objects.get(pk=created.id)

        self.assertEqual(updated.get_username(), self.update_data.get('username'))
        self.assertEqual(updated.email, self.update_data.get('email'))
