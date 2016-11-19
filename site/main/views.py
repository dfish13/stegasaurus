"""
 This file was created on October 15th, 2016
 by Deborah Venuti, Bethany Sanders and James Riley

 Contributors: Deborah Venuti, Bethany Sanders,
  James Riley, Gene Ryasnianskiy, Alexander Sumner

Last updated on: November 12, 2016
Updated by: Alexander Sumner
"""

#Python Imports
import tarfile
import os

#Django Imports
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files import File
from django.shortcuts import render, render_to_response, reverse
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView

#App Imports
from .models import stegaImage, stegaExtractedFile, stegaFile, tempFile
from .forms import RegisterForm, SignInForm, ImageForm, TextForm, TextDecryptForm, ImageDecryptForm, MultipleDataForm
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
# Alex Sumner modified to accept multiple images and tar them 
@login_required(login_url='main/signin.html')
def encrypt(request):
    title = 'Encrypt'

    userObject = User.objects.get(username = request.user.username)
    #print(userObject
    # Handle file upload
    if request.method == 'POST':
        
        #create form objects
        multiple_data_form = MultipleDataForm(request.POST, request.FILES)
        text_form = TextForm(request.POST, request.FILES)

        
        #form for gathering files and inserting them into a carrier
        if multiple_data_form.is_valid():
            
            #grab the information from the submitted form
            output = ContentFile(bytes(0))
            carrier = multiple_data_form.cleaned_data['carrier']
            tFile = tarfile.open("Data.tar", 'w')
            
            #temporarily store the files to facilitate taring them later
            for each in multiple_data_form.cleaned_data['Files']:
                newfile = tempFile(uploader=request.user)
                newfile.file.save(each.name, each)
                tFile.add(("./static" + newfile.file.url), arcname=each.name)
            
            #close the tar file and clean out temp data
            tFile.close()
            tempFile.objects.all().delete()
            
            #open file opject to grab the tar file
            data = open('Data.tar', mode = 'r+b')
            datas = File(data)

            #insert the data into the carrier
            stega.inject_file(carrier, datas.file , output)
            
            #save the tar file if we want to use it later
            newdata = stegaFile(uploader=request.user)
            newdata.file.save(datas.name, datas.file)

            #close the file objects and delete the temp tar file
            datas.close()
            data.close()
            os.remove(data.name)

            #save the steganographed image to the users database
            newimage = stegaImage(uploader=request.user)
            newimage.image.save(carrier.name, output)
            
            #return to the page
            return HttpResponseRedirect(reverse('encrypt'))

        #form for text insertion
        if text_form.is_valid():
            
            #grab information from the submitted form
            output = ContentFile(bytes(0))
            carrier = text_form.cleaned_data['carrier']
            text = text_form.cleaned_data['text']
            
            #inject the text into the image
            stega.inject_text(carrier, text , output)
            
            #save the steganographed image into the users database
            new = stegaImage(uploader=request.user)
            new.image.save(carrier.name, output)
            
            #return to the page
            return HttpResponseRedirect(reverse('encrypt'))

    else:
        #set defaults for when no data has been submitted
        multiple_data_form = MultipleDataForm()
        text_form = TextForm()


    # Load documents for the list page
    documents = stegaImage.objects.all().filter(uploader = request.user)

    #create list of information to send over the the .html file
    context = {
        'documents': documents,
        'multiple_data_form': multiple_data_form,
        'text_form': text_form,
        'title': title,
        }
    
    #load the page
    return render(request, 'main/encrypt.html', context)


#Alexander Sumner - tab for decrypting images 
@login_required(login_url='main/signin.html')
def decrypt(request):
    title = 'Decrypt'

    #gather user information
    userObject = User.objects.get(username = request.user.username)

    if (request.method == 'POST'):
        
        #create form objects
        text_decrypt_form = TextDecryptForm(request.POST, request.FILES)
        image_decrypt_form = ImageDecryptForm(request.POST, request.FILES)

        #form for extracting text
        if text_decrypt_form.is_valid():
            carrier = text_decrypt_form.cleaned_data['carrier']
            text_decrypt_form.message = stega.extract_text(carrier)


        #form for extracting images/other files
        if image_decrypt_form.is_valid():
            output = ContentFile(bytes(0))
            carrier = image_decrypt_form.cleaned_data['carrier']
            
            #extracting is currently in development
            stega.extract_file(carrier, output)
            
            #save the extracted file to the users database
            new = stegaExtractedFile(uploader=request.user)
            new.file.save(carrier.name, output)
            
            return HttpResponseRedirect(reverse('decrypt'))
    
    else:
        text_decrypt_form = TextDecryptForm()
        image_decrypt_form = ImageDecryptForm()


    context = {
        'image_decrypt_form': image_decrypt_form,
        'text_decrypt_form': text_decrypt_form,
        'title': title,
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
