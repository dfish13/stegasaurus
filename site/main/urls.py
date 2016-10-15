from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about', views.about, name='about'),
    url(r'^profile', views.profile, name='profile'),
    url(r'^signin', views.signin, name='signin'),
    url(r'^register', views.register, name='register'),
]
