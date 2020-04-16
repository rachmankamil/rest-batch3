# app.py


from blueprints.person.resources import bp_person
from blueprints.client.resources import bp_client
from flask import Flask
from flask_restful import Resource, Api
import json

app = Flask(__name__)
## initiate flask-restful instance
api = Api(app)

####################################
# Import blueprints
####################################
app.register_blueprint(bp_person, url_prefix='/person')
app.register_blueprint(bp_client, url_prefix='/client')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
