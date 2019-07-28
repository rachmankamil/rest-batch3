import json
from datetime import timedelta
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config['APP_DEBUG'] = True

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

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:masukaja@127.0.0.1/rest_training'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

####################################
# Middlewares
######################################

@app.after_request
def after_request(response):
    if request.method == 'GET':
        app.logger.warning("REQUEST_LOG\t%s", json.dumps({'request': request.args.to_dict(
        ), 'response': json.loads(response.data.decode('utf-8'))}))
    else:
        app.logger.warning("REQUEST_LOG\t%s", json.dumps(
            {'request': request.get_json(), 'response': json.loads(response.data.decode('utf-8'))}))
    return response

####################################
# Import blueprints
####################################

from blueprints.person.resources import bp_person
from blueprints.auth import bp_auth

app.register_blueprint(bp_person, url_prefix='/person')
app.register_blueprint(bp_auth, url_prefix='/token')

db.create_all()
