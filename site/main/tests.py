"""
 This file was created on October 18th, 2016
 by Jennifer Yarboro

 Last updated on: November 9th, 2016
 Updated by: Jennifer Yarboro
"""


from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from . import views

from .forms import MultipleDataForm, DecryptForm, TextForm, DeleteFileForm
from multiupload.fields import MultiFileField
from django import forms

#this class mostly tests views
#should be able to seperately test the views and other
#page functionality in later iterations

class TestCalls(TestCase):

	#test index page
	def test_index_view_loads(self):
		self.client.login(userName='test@steg.com', userPassword='testpassword')
		response = self.client.get('/', follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/index.html')		

	#test about page
	def test_about_view_loads(self):
		self.client.login(userName='test@steg.com', userPassword='testpassword')
		response = self.client.get('/about', follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/about.html')

#------------ PROFILE PAGE TESTS -------------

	#test redirect profile access
	def test_profile_view_invalid(self):
		self.user = User.objects.create_user(username='test@steg.com', password='testpassword')
		self.user.save()

		self.client.login(username='fake@steg.com', userpassword='fake')
		response = self.client.get('/profile', follow=False)
		self.assertEqual(response.status_code, 302)

	#test profile access
	def test_profile_view_valid(self):
		self.user = User.objects.create_user(username='test@steg.com', password='testpassword')
		self.user.save()

		self.client.login(username='test@steg.com', password='testpassword')
		response = self.client.get('/profile', follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/profile.html')

#------------ ENCRYPT PAGE TESTS -------------

	#test encrypt redirect access
	def test_encrypt_view_invalid(self):
		self.user = User.objects.create_user(username='test@steg.com', password='testpassword')
		self.user.save()

		self.client.login(username='fake@steg.com', userpassword='fake')
		response = self.client.get('/encrypt', follow=False)
		self.assertEqual(response.status_code, 302)

	#test encrypt access
	def test_encrypt_view_valid(self):
		self.user = User.objects.create_user(username='test@steg.com', password='testpassword')
		self.user.save()

		self.client.login(username='test@steg.com', password='testpassword')
		response = self.client.get('/decrypt', follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/decrypt.html')


#------------ DECRYPT PAGE TESTS -------------

	#test decrypt redirect access
	def test_decrypt_view_invalid(self):
		self.user = User.objects.create_user(username='test@steg.com', password='testpassword')
		self.user.save()

		self.client.login(username='fake@steg.com', userpassword='fake')
		response = self.client.get('/decrypt', follow=False)
		self.assertEqual(response.status_code, 302)

	#test decrypt access
	def test_decrypt_view_valid(self):
		self.user = User.objects.create_user(username='test@steg.com', password='testpassword')
		self.user.save()

		self.client.login(username='test@steg.com', password='testpassword')
		response = self.client.get('/decrypt', follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/decrypt.html')	


#------------ LOGIN PAGE TESTS -------------

	#test signin page
	def test_signin_view_loads(self):
		self.client.login(username='test@steg.com', userpassword='testpassword')
		response = self.client.get('/signin')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/signin.html')

	#test valid login
	def test_signin_view_valid(self):
		self.client.login(username='test@steg.com', userpassword='testpassword')
		response = self.client.post('/signin', {'username':'test@steg.com', 'password':'testpassword'}, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/signin.html')

	#test invalid login
	def test_signin_view_invalid(self):
		self.client.login(username='test@steg.com', userpassword='testpassword')
		response = self.client.post('/signin', {'username':'test@steg.com', 'password':'badpass'}, follow=False)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/signin.html')

	#test blank login message
	def test_call_view_fails_blank(self):
		self.client.login(userName='test@steg.com', userPassword='testpassword')
		response = self.client.post('/signin', {})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/signin.html')


#------------ REGISTER PAGE TESTS -------------

	#test register view
	def test_call_register_view(self):
		response = self.client.post('/register', {'first_name':'new', 'last_name':'user', 'email':'newuser@steg.com', 'password':'newpassword'})
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/signin')

	#test blank register
	def test_blank_register_view(self):
		response = self.client.post('/register', {'first_name':'', 'last_name':'', 'email':'', 'password':''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/register.html')


#-------------------------END OF TEST SUITE----------------------