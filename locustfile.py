from locust import HttpUser, task

from random import randint
from faker import Faker

from datetime import datetime

fake: Faker = Faker()


class CustomerViewSetLoadTests(HttpUser):

    @task
    def list(self):
        self.client.get('/api/customers/')

    @task
    def retrieve(self):
        self.client.get(f'/api/customers/{randint(0, 100)}/')

    @task
    def create(self):

        username = fake.name().replace(' ', '')
        data = {
            'username': username,
            'email': f'{username}@{username}.dev',
            'is_staff': False
        }

        self.client.post('/api/customers/', data=data)

    @task
    def update(self):
        username = fake.name().replace(' ', '')
        data = {
            'username': username,
            'email': f'{username}@{username}.dev',
            'password': fake.text(),
            'is_staff': False
        }

        self.client.put(f'/api/customers/{randint(0, 100)}/', data=data)

    @task
    def partial_update(self):
        username = fake.name().replace(' ', '')
        data = {
            'username': username,
        }

        self.client.patch(f'/api/customers/{randint(0, 100)}/', data=data)

    @task
    def destroy(self):
        self.client.delete(f'/api/customers/{randint(0, 100)}/')


class CartViewSetLoadTests(HttpUser):

    @task
    def create(self):
        data = {
            'customer': randint(0, 100),
            'product': randint(0, 100)
        }

        self.client.post('/api/carts/', data=data)

    @task
    def retrieve(self):
        self.client.get(f'/api/carts/{randint(0, 100)}/')


class OAuthApiViewLoadTests(HttpUser):

    @task
    def access(self):
        data = {
            'username': fake.name().replace(' ', ''),
            'password': fake.text(),
            'grant_type': 'password',
            'client_secret': fake.text(),
            'client_id': fake.text()
        }

        self.client.post(
            url='/api/o/custom/',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=data
        )


class PriceViewSetLoadTests(HttpUser):

    @task
    def list(self):
        self.client.get('/api/prices/')

    @task
    def create(self):
        data = {
            'product': randint(0, 100),
            'price': randint(100, 500)
        }

        self.client.post('/api/prices/', data=data)

    @task
    def retrieve(self):
        self.client.get(f'/api/prices/{randint(0, 100)}/')

    @task
    def destroy(self):
        self.client.delete(f'/api/prices/{randint(0, 100)}/')


class ProductViewSetLoadTests(HttpUser):

    @task
    def list(self):
        self.client.get('/api/products/')

    @task
    def create(self):
        data = {
            'name': fake.name(),
            'description': fake.text(),
            'category': randint(1, 5),
            'supplier': randint(0, 100),
            'price': randint(100, 500)
        }

        self.client.post('/api/products/', data=data)

    @task
    def retrieve(self):
        self.client.get(f'/api/products/{randint(0, 100)}/')

    @task
    def partial_update(self):
        data = {
            'name': fake.name(),
            'description': fake.text(),
            'category': randint(1, 5)
        }

        self.client.patch(f'/api/products/{randint(0, 100)}/', data=data)

    @task
    def delete(self):
        self.client.delete(f'/api/products/{randint(0, 100)}/')

    @task
    def recommendation(self):
        self.client.get(f'/api/products/categories/{randint(0, 100)}/')


class ReviewViewSetLoadTests(HttpUser):

    @task
    def list(self):
        self.client.get('/api/reviews/')

    @task
    def create(self):
        data = {
            'product': randint(0, 100),
            'customer': randint(0, 100),
            'value': randint(0, 6)
        }
        self.client.post('/api/reviews/', data=data)

    @task
    def partial_update(self):
        data = {
            'value': randint(0, 6)
        }
        self.client.patch(f'/api/reviews/{randint(0, 100)}/', data=data)

    @task
    def destroy(self):
        self.client.delete(f'/api/reviews/{randint(0, 100)}/')


class SaleViewSetLoadTests(HttpUser):

    @task
    def list(self):
        self.client.get('/api/sales/')

    @task
    def create(self):
        data = {
            'customer': randint(0, 100),
            'products': [randint(0, 100) for _ in range(10)],
            'delivery_address': fake.address(),
            'payment_method': randint(1, 4)
        }

        self.client.post('/api/sales/', data=data)

    @task
    def retrieve(self):
        self.client.get(f'/api/sales/{randint(0, 100)}/')


class SupplierViewSetLoadTests(HttpUser):

    @task
    def list(self):
        self.client.get('/api/suppliers/')

    @task
    def create(self):
        data = {
            'name': fake.name(),
            'address': fake.address(),
            'phone': fake.phone_number()
        }

        self.client.post('/api/suppliers/', data=data)

    @task
    def retrieve(self):
        self.client.get(f'/api/suppliers/{randint(0, 100)}/')

    @task
    def partial_update(self):
        data = {
            'name': fake.name()
        }
        self.client.patch(f'/api/suppliers/{randint(0, 100)}/', data=data)

    @task
    def destroy(self):
        self.client.delete(f'/api/suppliers/{randint(0, 100)}/')


class TagViewSetLoadTests(HttpUser):

    @task
    def list(self):
        self.client.get('/api/tags/')

    @task
    def create(self):
        data = {
            'name': fake.name(),
            'product': randint(0, 100)
        }
        self.client.post('/api/tags/', data=data)

    @task
    def destroy(self):
        self.client.delete(f'/api/tags/{fake.name()}/')


class TokenViewSetLoadTests(HttpUser):

    @task
    def generate(self):
        self.client.get(
            url='/api/token/',
            headers={'Authorization': f'Bearer {fake.text()}'}
        )

    @task
    def refresh(self):
        data = {
            'refresh': fake.text()
        }

        self.client.post('/api/token/refresh/', data=data)
