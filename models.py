# from app import app
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Posts(db.Model):
    __table_args__ = {'extend_existing': True} 

    _id = db.Column("id", db.Integer, primary_key=True)
    headline = db.Column("headline", db.String(200))
    textarea = db.Column("text", db.String(4000))
    date_created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, headline, textarea):
        self.headline = headline
        self.textarea = textarea

class Users(db.Model):
    __table_args__ = {'extend_existing': True} 

    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("username", db.String(20), unique=True, nullable=False)
    password = db.Column("password", db.String(4000), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def __getitem__(self, key):
        return self.__dict__[key]

    

    
