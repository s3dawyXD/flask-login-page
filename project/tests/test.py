import unittest
from project import app

class ProjectTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEquals(app.debug, False)
    
    def tearDown(self):
        pass

    def test_login_page(self):
        res = self.app.get('/', follow_redirects=True)
        self.assertIn(b'LOGIN', response.data)

if __name__ == "__main__":
    unittest.main()
