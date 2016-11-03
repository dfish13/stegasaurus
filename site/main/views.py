"""
 This file was created on October 15th, 2016
 by Deborah Venuti, Bethany Sanders and James Riley

 Contributors: Deborah Venuti, Bethany Sanders,
  James Riley, Gene Ryasnianskiy

Last updated on: November 1, 2016
Updated by: Duncan Fisher
"""

#Django Imports
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.shortcuts import render, render_to_response, reverse
from django.shortcuts import get_object_or_404

#App Imports
from .models import stegaImage
from .forms import RegisterForm, SignInForm, ImageForm, TextForm
from . import stega

def index(request):
    return render(request, 'main/index.html')

def about(request):
    title = 'About'
    return render(request, 'main/about.html', {'title': title})

# Deborah Venuti added login_required decorator
@login_required(login_url='main/signin.html')
def profile(request):
    title = 'Profile'
    return render(request, 'main/profile.html', {'title': title})

# Deborah Venuti added this
# Gene Ryasnianskiy image upload and processing
@login_required(login_url='main/signin.html')
def encrypt(request):
    title = 'Encrypt'

    userObject = User.objects.get(username = request.user.username)
    #print(userObject)
    # Handle file upload
    if request.method == 'POST':
        image_form = ImageForm(request.POST, request.FILES)
        text_form = TextForm(request.POST, request.FILES)
        if image_form.is_valid():

            output = ContentFile(bytes(0))
            carrier = image_form.cleaned_data['carrier']
            data_file = image_form.cleaned_data['data_file']
            stega.inject_file(carrier, data_file , output)
            new = stegaImage(uploader=request.user)
            new.image.save(carrier.name, output, save=True )
            return HttpResponseRedirect(reverse('profile'))

        if text_form.is_valid():
            pass
    else:
        image_form = ImageForm()
        text_form = TextForm()


    # Load documents for the list page
    documents = stegaImage.objects.all().filter(uploader = request.user)

    return render(request, 'main/encrypt.html', {'documents': documents, 'image_form': image_form, 'text_form': text_form, 'title':title})

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
