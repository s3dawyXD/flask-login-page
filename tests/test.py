import unittest
from project import app
import json

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
        self.assertIn(b'LOGIN', res.data)
    def test_login(self):
        res = self.app.post('/login',json = {'userName':'mohamed','password':'hello'},follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.data)
        self.assertTrue(body.get("success"))

if __name__ == "__main__":
    unittest.main()
