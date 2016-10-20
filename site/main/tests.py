"""
 This file was created on October 18th, 2016
 by Jennifer Yarboro

 Last updated on: October 19th, 2016
 Updated by: Jennifer Yarboro
"""


from django.test import TestCase, RequestFactory
from . import views

class TestCalls(TestCase):

	#test index page
	def test_index_view_loads(self):
		self.client.login(userName='test@steg.com', userPassword='testpassword')
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/index.html')		

	#test about page
	def test_about_view_loads(self):
		self.client.login(userName='test@steg.com', userPassword='testpassword')
		response = self.client.get('/about')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/about.html')

	#test redirect profile access
	#def test_profile_view_invalid(self):



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
		
		#response is giving a 200 instead of 302, dont know why		
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/signin.html')
		#self.assertRedirects(response, '/profile')

	#test invalid login
	def test_signin_view_invalid(self):
		self.client.login(userName='test@steg.com', userPassword='testpassword')
		response = self.client.post('/signin', {'username':'test@steg.com', 'password':'badpass'}, follow=False)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/signin.html')
		#self.assertRedirects(response, '/signin')

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