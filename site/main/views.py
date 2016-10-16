"""
 This file was created on October 15th, 2016
 by Deborah Venuti, Bethany Sanders and James Riley

 Last updated on: October 15th, 2016
 Updated by: Deborah Venuti
"""

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render, render_to_response
from django.template import RequestContext

from .forms import RegisterForm, SignInForm

def index(request):
    return render(request, 'main/index.html')

def about(request):
    title = 'About'
    return render(request, 'main/about.html', {'title': title})

def profile(request):
    title = 'Profile'
    return render(request, 'main/profile.html', {'title': title})

def signin(request):
    title = 'Sign In'

    # We need to process the registration form data
    form = SignInForm(request.POST)
    
    # Check if valid
    if form.is_valid():
        
        return HttpResponseRedirect('/profile')

    else:
        form = SignInForm()

    return render(request, 'main/signin.html', {'form': form, 'title': title})

def register(request):
    title = 'Register'

    form = RegisterForm(request.POST)

    if form.is_valid():
        return HttpResponseRedirect('Success')

    else:
        form = RegisterForm()

    return render(request, 'main/register.html', {'form': form, 'title':title})




