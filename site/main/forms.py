"""
 This file was created on October 15th, 2016
 by Deborah Venuti

 Contributors: Deborah Venuti, Gene Ryasnianskiy, Alexander Sumner


 Last updated on: November 20, 2016
 Updated by: Gene Ryasnianskiy
"""

from django import forms
from multiupload.fields import MultiFileField

class RegisterForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    email = forms.EmailField(label='Email', max_length=150)
    password = forms.CharField(label='Password', max_length=32, widget=forms.PasswordInput)

class SignInForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=150)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

# Added: Gene Ryasnianskiy October 31, 2016
class TextForm(forms.Form):
    carrier = forms.ImageField()
    text = forms.CharField(widget=forms.Textarea)

class DecryptForm(forms.Form):
    TEXT = 'T'
    FILE = 'F'
    carrier = forms.ImageField(label='Encrypted Image')
    choice = forms.ChoiceField(
        choices = (
            (TEXT, 'Decrypt Text'),
            (FILE, 'Decrypt File')
            )
        )

class MultipleDataForm(forms.Form):
    carrier = forms.ImageField(label='Carrier File')
    Files = MultiFileField(label='Data Files')

#Added: Gene Ryasnianskiy November 20, 2016
class DeleteFileForm(forms.Form):
    delete = forms.MultipleChoiceField(
        #choices = LIST_OF_VALID_CHOICES,
        widget  = forms.CheckboxSelectMultiple,
    )
