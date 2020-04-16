import json, config
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

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
app.register_blueprint(bp_person, url_prefix='/person')

db.create_all()
