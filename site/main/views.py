from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template('main/index.html')
    return HttpResponse(template.render(request))

def signin(request):
    template = loader.get_template('main/signin.html')
    return HttpResponse(template.render(request))

def register(request):
    template = loader.get_template('main/register.html')
    return HttpResponse(template.render(request))

