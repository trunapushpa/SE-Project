from flask import Flask
from config import Config, ProductionConfig, DevelopmentConfig, TestingConfig
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)

from application import routes