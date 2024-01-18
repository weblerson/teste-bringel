from django.contrib import admin
from .models import Customer
from .forms import CustomerChangeForm, CustomerCreationForm

from django.contrib.auth.admin import UserAdmin


@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    form = CustomerChangeForm
    add_form = CustomerCreationForm
    model = Customer
