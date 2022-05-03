from flask_login import UserMixin
from . import db

#User model taken and modified from digital ocean
# https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login#step-5-creating-user-models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    userType = db.Column(db.String(100)) #Recruiter #JobSeeker
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    history = db.relationship('History', backref='user', lazy=True)

#History class created  by myself, used to track files user has created.
class History(db.Model):
    postID = db.Column(db.Integer, primary_key=True) 
    userID = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    fileName = db.Column(db.String(1000))
