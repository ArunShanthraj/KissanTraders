from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import CustomerTransaction, Customer


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TransactionForm(ModelForm):
    class Meta:
        model = CustomerTransaction
        fields = '__all__'


class AddCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone']
