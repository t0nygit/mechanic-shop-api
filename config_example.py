from urllib.parse import quote_plus

class Config:
    password = quote_plus('YOUR_MYSQL_PASSWORD_HERE')
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://root:{password}@localhost/mechanic_shop'
    SQLALCHEMY_TRACK_MODIFICATIONS = False