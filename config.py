import os
from urllib.parse import quote_plus

class Config:
    password = quote_plus(os.environ.get('MYSQL_PASSWORD', 'default'))
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://root:{password}@localhost/mechanic_shop'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False