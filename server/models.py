from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
import datetime
db = SQLAlchemy()

def get_uuid():
    return uuid4().hex

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(32),primary_key= True,unique = True,default = get_uuid)
    name = db.Column(db.String(345),nullable=False)
    email = db.Column(db.String(345),unique= True)
    password = db.Column(db.Text,nullable=False)
    address = db.Column(db.String(345),nullable=False)
    verified_user = db.Column(db.Boolean, default=False, nullable=False)
    created_on = db.Column(db.DateTime,default=datetime.datetime.now())
    
class EmailAnalytics(db.Model):
    __tablename__ = "email_analytics"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True, index = True,nullable = False)
    email = db.Column(db.String(345),nullable=False)
    last_sent_on = db.Column(db.DateTime,default=datetime.datetime.now())
    email_delivered = db.Column(db.Boolean, default=True, nullable=False)
    email_opened = db.Column(db.Boolean, default=False, nullable=False)
