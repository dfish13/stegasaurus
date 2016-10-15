from django import forms

class RegisterForm(forms.Form):
    full_name = forms.CharField(label='Full Name', max_length=100)
    email = forms.EmailField(label='Email', max_length=150)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

class SignInForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=150)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
