# -----------------------------------------------------------------------------------------------
#
#       Company:    Personal Research
#       By:         Fredrick Stakem
#       Created:    8.10.16   
#
# -----------------------------------------------------------------------------------------------


# Libraries
import json
import os
import sys
import logging

from flask import Flask
from celery import Celery

from micro_service import app_path
from micro_service.api.version_1_0_0 import app_v1_0_0
from micro_service.api.version_2_0_0 import app_v2_0_0
from micro_service.db.models.file_upload import FileUpload


# Framework globals
# -----------------------------------------------------
flask_app = None
current_app = app_v2_0_0
allowed_ext = set()


# Helper functions
# -----------------------------------------------------
def read_config(config_path):
    with open(config_path) as data_file:
        data = json.load(data_file)

    return data

def load_config(env):
    try:
        config_path = os.path.join(app_path, 'config', env + '.json')
        config = read_config(config_path)
    except FileNotFoundError as e:
        # TODO - handle
        sys.exit(-1)

    return config

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in allowed_ext

def setup_logger(config):
    # TODO - create app logger
    logger = None
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.ERROR)

    return logger

def create_flask_app(config):
    global allowed_ext
    db_password = os.environ['DB_PASSWORD']
    allowed_ext = set(config['allowed_file_ext'])
    db_connect_str = 'postgresql://{}:{}@{}/{}'.format(config['db_user'], db_password, config['db_host'], config['db_name'])

    flask_app = Flask(__name__)
    flask_app.secret_key                                = 'TTS96tKYthZh2V2jO7Bwi1c4BO0BFYfe8YnDegkg'
    flask_app.config['UPLOAD_FOLDER']                   = config['upload_folder']
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  = False
    flask_app.config['SQLALCHEMY_DATABASE_URI']         = db_connect_str
    flask_app.config['CELERY_BROKER_URL']               = 'amqp://guest@localhost:5672//'
    flask_app.config['CELERY_RESULT_BACKEND']           = 'amqp'

    return flask_app

def register_versions(flask_app):
    flask_app.register_blueprint(app_v1_0_0, url_prefix='/v1_0_0')
    flask_app.register_blueprint(app_v2_0_0, url_prefix='/v2_0_0')
    flask_app.register_blueprint(current_app)
    current_app

def create_celery(flask_app):
    celery = Celery(flask_app.name, 
        backend=flask_app.config['CELERY_RESULT_BACKEND'], 
        broker=flask_app.config['CELERY_BROKER_URL'])
    celery.conf.update(flask_app.config)

    return celery
