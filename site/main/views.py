"""
 This file was created on October 15th, 2016
 by Deborah Venuti, Bethany Sanders and James Riley

 Contributors: Deborah Venuti, Bethany Sanders,
  James Riley, Gene Ryasnianskiy, Alexander Sumner

Last updated on: November 3, 2016
Updated by: Alexander Sumner
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
from .models import stegaImage, stegaExtractedFile
from .forms import RegisterForm, SignInForm, ImageForm, TextForm, CarrierForm, ImageDecryptForm
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
        carrier_form = CarrierForm(request.POST, request.FILES)
        
        if image_form.is_valid():
            output = ContentFile(bytes(0))
            carrier = image_form.cleaned_data['carrier']
            data_file = image_form.cleaned_data['data_file']
            stega.inject_file(carrier, data_file , output)
            new = stegaImage(uploader=request.user)
            new.image.save(carrier.name, output, save=True )
            return HttpResponseRedirect(reverse('encrypt'))

        if text_form.is_valid():
            output = ContentFile(bytes(0))
            carrier = text_form.cleaned_data['carrier']
            text = text_form.cleaned_data['text']
            stega.inject_text(carrier, text , output)
            new = stegaImage(uploader=request.user)
            new.image.save(carrier.name, output, save=True )
            return HttpResponseRedirect(reverse('encrypt'))

        if carrier_form.is_valid():
            carrier = text_form.cleaned_data['carrier']
            message = stega.extract_text(carrier)

    else:
        message = ''
        image_form = ImageForm()
        text_form = TextForm()
        carrier_form = CarrierForm()


    # Load documents for the list page
    documents = stegaImage.objects.all().filter(uploader = request.user)
    context = {
        'documents': documents,
        'image_form': image_form,
        'text_form': text_form,
        'carrier_form': carrier_form,
        'title': title,
        'message': message,
        }
    return render(request, 'main/encrypt.html', context)

#Alexander Sumner - tab for decrypting images 
@login_required(login_url='main/signin.html')
def decrypt(request):
    title = 'Decrypt'

    #gather user information
    userObject = User.objects.get(username = request.user.username)

    if (request.method == 'POST'):
        carrier_form = CarrierForm(request.POST, request.FILES)
        image_decrypt_form = ImageDecryptForm(request.POST, request.FILES)

        #form for extracting text
        if carrier_form.is_valid():
            carrier = carrier_form.cleaned_data['carrier']
            message = stega.extract_text(carrier)


        #form for extracting images/other files
        if image_decrypt_form.is_valid():
            output = ContentFile(bytes(0))
            carrier = image_decrypt_form.cleaned_data['carrier']
            #extracting is currently in development
            stega.extract_file(carrier, output)
            new = stegaExtractedFile(uploader=request.user)
            new.image.save(carrier.name, output, save=True )
            return HttpResponseRedirect(reverse('decrypt'))
    
    else:
        message = ''
        carrier_form = CarrierForm()
        image_decrypt_form = ImageDecryptForm()


    context = {
        #'documents': documents,
        'image_decrypt_form': image_decrypt_form,
        'carrier_form': carrier_form,
        'title': title,
        'message': message,
        }

    return render(request, 'main/decrypt.html', context)



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
