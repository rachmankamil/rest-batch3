import json, os
from datetime import timedelta
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config['APP_DEBUG'] = True
app.config['PROPOGATE_EXCEPTIONS'] = True

####################################
# JWT
####################################

app.config['JWT_SECRET_KEY'] = 'SFsieaaBsLEpecP675r243faM8oSB2hV'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

# jwt custom decorator
@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {
        'claims': identity,
        'identifier': "ATA-BATCH3"
    }

####################################
# Database
####################################

try:
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:masukaja@127.0.0.1/rest_training_test'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:masukaja@127.0.0.1/rest_training'
except Exception as e:
    raise e

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:masukaja@127.0.0.1/rest_training'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

####################################
# Middlewares
######################################

@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    if response.status_code == 200:
        app.logger.info("REQUEST_LOG\t%s",
            json.dumps({
                'status_code': response.status_code,
                'method': request.method,
                'code': response.status,
                'uri': request.full_path,
                'request': requestData,
                'response': json.loads(response.data.decode('utf-8'))
            })
        )
    else:
        app.logger.error("REQUEST_LOG\t%s",
            json.dumps({
                'status_code': response.status_code,
                'method': request.method,
                'code': response.status,
                'uri': request.full_path,
                'request': requestData,
                'response': json.loads(response.data.decode('utf-8'))
            })
        )
    return response

####################################
# Import blueprints
####################################

from blueprints.person.resources import bp_person
from blueprints.auth import bp_auth
from blueprints.weather.resources import bp_weather

app.register_blueprint(bp_person, url_prefix='/person')
app.register_blueprint(bp_auth, url_prefix='/token')
app.register_blueprint(bp_weather, url_prefix='/weather')

db.create_all()
