from dotenv import load_dotenv
import os
import redis
load_dotenv()

class ApplicationConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/zippee'

    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_COOKIE_SAMESITE="None"
    SESSION_COOKIE_SECURE=True
    SESSION_USER_SIGNER = True
    SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")

    # configuration of mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'fellasniperbot@gmail.com'
    MAIL_PASSWORD = 'vjoritoicnkpfeec'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True