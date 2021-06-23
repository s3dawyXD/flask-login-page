import unittest
from project import app, db
import json
from flask_sqlalchemy import SQLAlchemy
from project.models import User

class ProjectTests(unittest.TestCase):

    def setUp(self):
        self.db_name = "temp_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.db_name)
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = self.database_path
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.db = db
        self.db.drop_all()
        self.db.create_all()
        self.app = app.test_client()
        self.assertEquals(app.debug, False)
        
        
    
    def tearDown(self):
        pass

    def test_login_page(self):
        res = self.app.get('/', follow_redirects=True)
        self.assertIn(b'LOGIN', res.data)
    
    def test_register_new_user(self):
        res = self.app.post('/register',json = {'userName':'test_user','password':'123'},follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.data)
        self.assertTrue(body.get("success"))
        user = User.query.filter_by(user_name='test_user').one_or_none()
        if(user):
            user.delete()
        else:
            self.assertFalse(True)
    
    def test_register_user_do_exist(self):
        res = self.app.post('/register',json = {'userName':'test_user','password':'123'},follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.data)
        self.assertTrue(body.get("success"))
        res = self.app.post('/register',json = {'userName':'test_user','password':'123'},follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.data)
        self.assertFalse(body.get("success"))
        user = User.query.filter_by(user_name='test_user').one_or_none()
        if(user):
            user.delete()
        else:
            self.assertFalse(True)
    
    def test_login(self):
        res = self.app.post('/register',json = {'userName':'test_user','password':'123'},follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.data)
        self.assertTrue(body.get("success"))
        res = self.app.post('/login',json = {'userName':'test_user','password':'123'},follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.data)
        self.assertTrue(body.get("success"))
        
        
        user = User.query.filter_by(user_name='test_user').one_or_none()
        if(user):
            user.delete()
        else:
            self.assertFalse(True)
    
    def test_profile(self):
        _ = self.app.post('/register',json = {'userName':'test_user','password':'123'},follow_redirects=True)
        res = self.app.post('/login',json = {'userName':'test_user','password':'123'},follow_redirects=True)
        body = json.loads(res.data)
        jwt = body.get("jwt")
        res = self.app.get('/profile', headers={"Authorization": 'bearer '+ jwt})
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.data)
        self.assertTrue(body.get("success"))

        user = User.query.filter_by(user_name='test_user').one_or_none()
        if(user):
            user.delete()
        else:
            self.assertFalse(True)
    

if __name__ == "__main__":
    unittest.main()
