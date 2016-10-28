"""
 This file was created on October 15th, 2016
 by Deborah Venuti, Bethany Sanders and James Riley

 Last updated on: October 28th, 2016
 Updated by: Deborah Venuti
"""

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response

from .forms import RegisterForm, SignInForm

def index(request):
    return render(request, 'main/index.html')

def about(request):
    title = 'About'
    return render(request, 'main/about.html', {'title': title})

# Deborah Venuti added login_required decorator
@login_required('main/signin.html')
def profile(request):
    title = 'Profile'
    return render(request, 'main/profile.html', {'title': title})

# Deborah Venuti added return of invalid indicator for sign in attempt of non-existing account
def signin(request):
    title = 'Sign In'

    if (request.method == 'POST'):
        form = SignInForm(request.POST)
        if form.is_valid():
            formData = form.cleaned_data
            userName = formData['email']
            userPassword = formData['password']

            user = authenticate(username=userName, password=userPassword)
            print(user)
            if (user is not None):
                login(request,user)
                return HttpResponseRedirect('/profile')
            else:
                return render(request, 'main/signin.html', {'form':form, 'invalid': True})

    else:
        form = SignInForm()
    return render(request, 'main/signin.html', {'form': form, 'title': title})

def register(request):
    title = 'Register'

    if (request.method == 'POST'):
        form = RegisterForm(request.POST)
        if form.is_valid():
            formData = form.cleaned_data

            try:
                user = User.objects.get(username=formData['email'])
            
            except User.DoesNotExist:
                user = User.objects.create_user(formData['email'], formData['email'], formData['password'], first_name=formData['first_name'], last_name=formData['last_name'])
                user.save()

            return HttpResponseRedirect('/signin')

    else:
        form = RegisterForm()

    return render(request, 'main/register.html', {'form': form, 'title':title})
