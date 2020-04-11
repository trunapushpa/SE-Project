import os

class Config(object):
    DEBUG = False
    TESTING = False
    DBPWD = 'lostnfound@12345'
    DBUSER = 'myadmin@lostnfounddb'
    DBNAME = 'lostnfound'
    DBSERVER = 'lostnfounddb.postgres.database.azure.com:5432'
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DBUSER}:{DBPWD}@{DBSERVER}/{DBNAME}" 
    #"dbname='lostnfound' user='myadmin@lostnfounddb' host='lostnfounddb.postgres.database.azure.com' password='lostnfound@12345' port='5432' sslmode='true'"

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True

class TestingConfig(Config):
    TESTING = True   