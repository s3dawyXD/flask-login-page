from project import db
from sqlalchemy import Column, String, Integer, create_engine


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    password = Column(String)
    

    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password
        

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
        'id': self.id,
        'UserName': self.user_name,
        'password': self.password
        }
