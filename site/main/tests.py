"""
 This file was created on October 18th, 2016
 by Jennifer Yarboro

 Last updated on: October 19th, 2016
 Updated by: Jennifer Yarboro
"""


from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from . import views

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

	#test signin page
	def test_signin_view_loads(self):
		self.client.login(userName='test@steg.com', userPassword='testpassword')
		response = self.client.get('/signin')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/signin.html')

	#test valid login
	def test_signin_view_valid(self):
		self.client.login(userName='test@steg.com', userPassword='testpassword')
		response = self.client.post('/signin', {'username':'test@steg.com', 'password':'testpassword'}, follow=True)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/signin.html')

	#test invalid login
	def test_signin_view_invalid(self):
		self.client.login(userName='test@steg.com', userPassword='testpassword')
		response = self.client.post('/signin', {'username':'test@steg.com', 'password':'badpass'}, follow=False)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/signin.html')

	#test blank login message
	#def test_call_view_fails_blank(self):
	#	self.client.login(userName='test@steg.com', userPassword='testpassword')
	#	response = self.client.post('/signin', {})
	#	self.assertFormError(response, 'form', 'fieldname', 'expected error message')

	#test invalid login message
	#def test_call_view_fails_blank(self):
	#	self.client.login(userName='test@steg.com', userPassword='testpassword')
	#	response = self.client.post('/signin', {'invaliduser':'invalidpass'})
	#	self.assertFormError(response, 'form', 'fieldname', 'expected error message')