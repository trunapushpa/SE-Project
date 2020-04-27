import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'1\xdc\x92N\xc9+n\xbf\x81<\xd7t\xca3\xe7b'
    DEBUG = False
    TESTING = False
    DBPWD = 'lostnfound@12345'
    DBUSER = 'myadmin@lostnfounddb'
    DBNAME = 'lostnfound'
    DBSERVER = 'lostnfounddb.postgres.database.azure.com:5432'
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DBUSER}:{DBPWD}@{DBSERVER}/{DBNAME}" 
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ASCRANKVALUES = [0, 5, 20, 50, 100]
    ASCRANKS = ['Rookie', 'Beginner', 'Skilled', 'Proficient', 'Expert']
    ASCRANKCOLORS = ['secondary', 'success', 'info', 'warning', 'danger']
    REWARD = {'lost': [1, 6], 'found': [6, 1], 'buy': [3, 3], 'sell': [3, 3], 'unsuccessful': 1}
    NOTIFY = {'lost': 'found', 'found': 'lost', 'buy': 'sell', 'sell': 'buy'}
    #"dbname='lostnfound' user='myadmin@lostnfounddb' host='lostnfounddb.postgres.database.azure.com' password='lostnfound@12345' port='5432' sslmode='true'"

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True

class TestingConfig(Config):
    TESTING = True   