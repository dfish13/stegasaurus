from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader

from .forms import RegisterForm, SignInForm

def index(request):
    template = loader.get_template('main/index.html')
    return HttpResponse(template.render(request))

def about(request):
    template = loader.get_template('main/about.html')
    return HttpResponse(template.render(request))

def signin(request):
    # We need to process the registration form data
    form = SignInForm(request.POST)

    # Check if valid
    if form.is_valid():
        # Process the data
        # Eventually redirect to user profile
        return HttpResponseRedirect('Successful Login.')

    else:
        form = SignInForm()

    return render(request, 'main/signin.html', {'form': form})


def register(request):
    # We need to process the registration form data
    form = RegisterForm(request.POST)

    # Check if valid
    if form.is_valid():
        # Process the data
        return HttpResponseRedirect('Registration Successful.')

    else:
        form = RegisterForm()

    return render(request, 'main/register.html', {'form': form})




