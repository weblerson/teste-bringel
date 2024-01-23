from rest_framework import test

from ..models import Cart
from ..serializers import CartSerializer

from authentication.serializers import CustomerSerializer
from products.serializers import ProductSerializer, SupplierSerializer

from authentication.models import Customer
from products.models import Product, Supplier


class CartSerializerTests(test.APITestCase):

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

        product_data = {
            'name': 'Test Science Product',
            'description': 'Test description',
            'category': Product.Category.SCIENCE,
            'supplier': supplier.id,
            'price': 100
        }
        product_serializer: ProductSerializer = ProductSerializer(data=product_data)
        product_serializer.is_valid()
        product: Product = product_serializer.save()

        cls.fields = ('id', 'customer', 'products')
        cls.customer = customer
        cls.product = product

    def test_if_cart_serializer_have_all_fields(self):
        """
        Tests if cart serializer have all fields (id, customer and products)
        """

        serializer: CartSerializer = CartSerializer()

        for field in serializer.fields:
            self.assertIn(field, self.fields)

    def test_if_cart_serializer_create_an_cart_instance_when_a_user_is_created(self):
        """
        Tests if cart serializer create a cart instance when a user is created
        """

        cart = Cart.objects.filter(pk=self.customer.id)

        self.assertTrue(cart.exists())
