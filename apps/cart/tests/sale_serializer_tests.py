from rest_framework import test

from ..models import Sale
from ..serializers import SaleSerializer

from authentication.serializers import CustomerSerializer
from products.serializers import ProductSerializer, SupplierSerializer

from authentication.models import Customer
from products.models import Product, Supplier, PriceHistory


class SaleSerializerTests(test.APITestCase):

    @classmethod
    def setUpTestData(cls):
        customer_data = {
            'username': 'John',
            'email': 'john@john.dev',
            'password': 'john',
            'is_staff': False
        }
        customer_serializer: CustomerSerializer = CustomerSerializer(data=customer_data)
        customer_serializer.is_valid()
        customer: Customer = customer_serializer.save()

        supplier_data = {
            'name': 'TestCia',
            'address': 'Test Address',
            'phone': '99999999999'
        }
        supplier_serializer: SupplierSerializer = SupplierSerializer(data=supplier_data)
        supplier_serializer.is_valid()
        supplier: Supplier = supplier_serializer.save()

        first_product_data = {
            'name': 'Test Science Product',
            'description': 'Test description',
            'category': Product.Category.SCIENCE,
            'supplier': supplier.id
        }
        second_product_data = {
            'name': 'Test Fiction Product',
            'description': 'Test description',
            'category': Product.Category.FICTION,
            'supplier': supplier.id
        }
        product_serializer: ProductSerializer = ProductSerializer(
            data=[first_product_data, second_product_data],
            many=True
        )
        product_serializer.is_valid()
        products = product_serializer.save()

        first_price = PriceHistory.objects.filter(product=products[0]).order_by('-start').first()
        second_price = PriceHistory.objects.filter(product=products[1]).order_by('-start').first()

        cls.fields = ('id', 'customer', 'products', 'total', 'delivery_address', 'payment_method', 'date')

        cls.test_data = {
            'customer': customer.id,
            'total': first_price + second_price,
            'delivery_address': 'Test Street',
            'payment_method': Sale.Payment.CREDIT
        }

    def test_if_sale_serializer_have_all_fields(self):
        """
        Tests if sale serializer have all fields (id, customer, products, total,
        delivery address, payment method and date)
        """

        serializer: SaleSerializer = SaleSerializer()

        for field in serializer.fields:
            self.assertIn(field, self.fields)

    def test_if_sale_serializer_create_an_sale_instance(self):
        """
        Tests if sale serializer create a sale instance
        """

        serializer: SaleSerializer = SaleSerializer(data=self.test_data)

        self.assertTrue(serializer.is_valid())

        sale: Sale = serializer.save()
        self.assertIsNotNone(sale)
