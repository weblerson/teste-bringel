from django.contrib.auth import forms
from .models import Customer

from typing import override


class CustomerChangeForm(forms.UserChangeForm):

    @override
    class Meta(forms.UserChangeForm.Meta):
        model = Customer


class CustomerCreationForm(forms.UserCreationForm):

    @override
    class Meta(forms.UserCreationForm.Meta):
        model = Customer
