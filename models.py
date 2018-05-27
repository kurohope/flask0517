from flask_sqlalchemy import SQLAlchemy
from flask import  Flask, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash
db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    register_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, *args, **kwargs):
        self.id=kwargs.get('id')
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.register_time = kwargs.get('register_time')


    #avatar_path = db.Column(db.String(256), nullable=False, default='images/doraemon.jpg')
class Questions(db.Model):
    __tablename__ = 'questions_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.TEXT, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users_info.id'))
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.title = kwargs.get('title')
        self.content = kwargs.get('content')
        self.author_id = kwargs.get('author_id')
        self.create_time = kwargs.get('create_time')


    author = db.relationship('Users', backref=db.backref('questions', order_by=create_time.desc()))
class Comments(db.Model):
    __tablename__ = 'comments_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.TEXT, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions_info.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users_info.id'))
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.content = kwargs.get('content')
        self.question_id = kwargs.get('question_id')
        self.author_id = kwargs.get('author_id')
        self.create_time = kwargs.get('create_time')

    author = db.relationship('Users', backref=db.backref('comments'))
    question = db.relationship('Questions', backref=db.backref('comments', order_by=create_time.desc()))

class MySession(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    s_id = db.Column(db.String(24), nullable=False)
    username = db.Column(db.String(64), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    expire_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.s_id = kwargs.get('s_id')
        self.username = kwargs.get('username')
        self.start_time = kwargs.get('start_time')
        self.expire_time = kwargs.get('expire_time')