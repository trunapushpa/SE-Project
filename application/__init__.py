import os
from flask import Flask
from flask_babel import Babel
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from config import Config, ProductionConfig, DevelopmentConfig, TestingConfig
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

UPLOAD_FOLDER = os.path.join('application', 'static', 'images', 'UploadedImages')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)
babel = Babel(app)
bootstrap = Bootstrap(app)

from application import routes