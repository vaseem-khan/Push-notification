import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django import forms
from listing.models import Product
from django.core import validators

class ProductForm(forms.ModelForm):
    title=forms.CharField(max_length=150, help_text="Please enter the title of the item")
    description=forms.CharField(max_length=10000, help_text="Please add a description")
    price=forms.FloatField(help_text="Please enter the price of item")
    
    class Meta:
        model=Product
        fields=('title','price','description','image1','image2','image3')



class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Please enter a desired username.")
    email = forms.CharField(help_text="Please enter your email.")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter a password.")
    password2 = forms.CharField(widget=forms.PasswordInput(), help_text="Please re-enter the password.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
    
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2