from django.test import TestCase

class TestCalls(TestCase):
	#def test_call_view_denies_anonymous_admin(self):
	#	response = self.client.get('/signin', follow=True)
	#	self.assertRedirects(response, 'main/signin.html')
	#	response = self.client.post('/signin', follow=True)
	#	self.assertRedirects(response, 'main/signin.html')

	def test_call_view_loads(self):
		self.client.login(userName='test@steg.com', userPassword='testpassword')
		response = self.client.get('/signin')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'main/signin.html')

	def test_call_view_fails_blank(self):
		self.client.login(userName='test@steg.com', userPassword='testpassword')
		response = self.client.post()