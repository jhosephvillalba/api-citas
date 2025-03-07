from dotenv import load_dotenv
import os

load_dotenv(override=True)

class Config(object):
    TESTING=False
    SECRET_KEY="dev"

class DevConfig(Config):
    DEBUG=True
    JWT_SECRET_KEY= os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI= os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS= os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False) == "True"
    
    # # print(SQLALCHEMY_DATABASE_URI)
    # MAIL_SERVER="smtp.ethereal.email"
    # MAIL_PORT=587
    # MAIL_USERNAME="yadira.barton@ethereal.email"
    # MAIL_PASSWORD="GvZ7VgvHd8YxDhD9fr"
    # MAIL_USE_TLS=True
    # MAIL_USE_SSL=False

class ProdConfig(Config):
    SECRET_KEY= os.getenv('SECRET_KEY')
    JWT_SECRET_KEY= os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI= os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS= os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS') == "True"

    # MAIL_SERVER="smtp.ethereal.email"
    # MAIL_PORT=587
    # MAIL_USERNAME="yadira.barton@ethereal.email"
    # MAIL_PASSWORD="GvZ7VgvHd8YxDhD9fr"
    # MAIL_USE_TLS=True
    # MAIL_USE_SSL=False
