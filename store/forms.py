from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Good
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, Field
import re


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        }),
        help_text=''  
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'id': 'login_id_username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login_id_password'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'id': 'login_id_remember_me'})
    )


class EmployeeLogin(forms.Form):
    employee_key = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'KEY',
            'id': 'login_id_employee_key'}))
    
class AddGoodForm(forms.ModelForm):

    class Meta:
        model = Good
        fields = ['name', 'category', 'price', 'description', 'img', 'stock', 'height', 'width', 'depth', 'weight', 'materials', 'style', 'color', 'accessories'] 

class DeleteGoodForm(forms.Form):

    name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Good name',
            'id': 'name'}))
    
class SearchQuery(forms.Form):
    query = forms.CharField(max_length=30)


class PlaceOrder(forms.Form):
    address = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
