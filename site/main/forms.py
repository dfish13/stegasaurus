"""
 This file was created on October 15th, 2016
 by Deborah Venuti

 Last updated on: October 15th, 2016
 Updated by: Deborah Venuti
"""

from django import forms

class RegisterForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    email = forms.EmailField(label='Email', max_length=150)
    password = forms.CharField(label='Password', max_length=32, widget=forms.PasswordInput)

class SignInForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=150)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
