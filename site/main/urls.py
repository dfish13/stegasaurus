"""
 This file was created on October 15th, 2016
 by Deborah Venuti and James Riley

 Last updated on: November 21st, 2016
 Updated by: Bethany Sanders
"""

from django.conf.urls import url
from django.contrib.auth.views import logout
from django.contrib.auth.views  import password_reset_done
from django.contrib.auth.views  import password_reset
from django.contrib.auth.views  import password_reset_confirm
from django.contrib.auth.views  import password_reset_complete

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about$', views.about, name='about'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^encrypt$', views.encrypt, name='encrypt'),
    url(r'^decrypt$', views.decrypt, name='decrypt'),
    url(r'^signin$', views.signin, name='signin'),
    url(r'^signout$', logout, {'next_page': '/'}, name='signout'),
    url(r'^register$', views.register, name='register'),
    url(r'^resetpassword/passwordsent$', password_reset_done, name = 'password_reset_done'),
    url(r'^resetpassword/$', password_reset, name = 'password_reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, name = 'password_reset_confirm'),
    url(r'^reset/done$', password_reset_complete, name = 'password_reset_complete'),
]
