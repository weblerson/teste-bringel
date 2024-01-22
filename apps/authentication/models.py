from django.db import models
from django.contrib.auth.models import AbstractUser


class Customer(AbstractUser):

    class Meta:
        verbose_name = 'Customer'
        ordering = ['id']
