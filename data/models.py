from flask_login import UserMixin
from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(45), unique=True, nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
