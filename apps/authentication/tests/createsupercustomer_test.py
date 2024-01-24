from django.core.management import call_command
from django.test import TestCase
from io import StringIO

from ..models import Customer


class CreateSuperCustomerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.username = 'admin'
        cls.password = 'admin'

    def test_if_command_is_creating_admin_customer(self):
        out = StringIO()
        call_command(f'createsupercustomer',
                     username=self.username,
                     password=self.password,
                     stdout=out)

        query = Customer.objects.filter(username=self.username)

        self.assertTrue(query.exists())
        customer: Customer = query.first()

        self.assertTrue(customer.is_superuser)
        self.assertTrue(customer.is_staff)
