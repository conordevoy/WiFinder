from WiFinderApp import WiFinderApp
import unittest

# test case for the WiFinderApp

class FlaskTestCase(unittest.TestCase):

	# test that status 200 is returned from a call to the site
	def test_index(self):
		tester = WiFinderApp.test_client(self)
		response = tester.get('/login', content_type='html/text')
		self.assertEqual(response.status_code, 200)

	# test that the site redirects with the login call first
	def test_redirect(self):
		tester = WiFinderApp.test_client(self)
		response = tester.get('/', content_type='html/text')
		self.assertEqual(response.status_code, 302)

	# test that the page loads and data is returned
	def test_index_page_loads(self):
		tester = WiFinderApp.test_client(self)
		response = tester.get('/login', content_type='html/text')
		self.assertTrue(b'WiFinder' in response.data)

	# test the login with correct login details
	def test_login_pass(self):
		tester = WiFinderApp.test_client(self)
		response = tester.post(
			'/login',
			data=dict(username="viewer", password="viewer"),
			follow_redirects=True
		)
		self.assertTrue(b'Logout' in response.data)

	# test that login fails with wrong details
	def test_login_fail(self):
		tester = WiFinderApp.test_client(self)
		response = tester.post(
			'/login',
			data=dict(username="wrong", password="wrong"),
			follow_redirects=True
		)
		self.assertTrue(b'Login' in response.data)

	# test that logout works after login
	def test_logout(self):
		tester = WiFinderApp.test_client(self)
		tester.post(
			'/login',
			data=dict(username="viewer", password="viewer"),
			follow_redirects=True
		)
		response = tester.get('/logout', follow_redirects=True)
		self.assertTrue(b'You have just been logged out!' in response.data)

	# test that you require to login, and that the user is informed of this
	def test_require_login(self):
		tester = WiFinderApp.test_client(self)
		response = tester.get('/', follow_redirects=True)
		self.assertTrue(b'Sorry, you need to login first!' in response.data) 

if __name__ == "__main__":
	unittest.main()