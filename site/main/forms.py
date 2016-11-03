"""
 This file was created on October 15th, 2016
 by Deborah Venuti

 Contributors: Deborah Venuti, Gene Ryasnianskiy, Alexander Sumner


 Last updated on: November 3, 2016
 Updated by: Alexander Sumner
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

# Added: Gene Ryasnianskiy October 31, 2016
class ImageForm(forms.Form):
    carrier = forms.ImageField(label='Carrier file')
    data_file = forms.FileField(label='Data file')

class TextForm(forms.Form):
    carrier = forms.ImageField()
    text = forms.CharField(widget=forms.Textarea)

class CarrierForm(forms.Form):
    carrier = forms.ImageField(label='Encrypted Image')

# Added: Alexander Sumner November 3, 2016
class ImageDecryptForm(forms.Form):
    carrier = forms.ImageField(label='Encrypted Image')