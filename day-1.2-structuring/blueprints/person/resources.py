from flask import Blueprint
from flask_restful import Api, reqparse, Resource

from . import Person

bp_person = Blueprint('person', __name__)
api = Api(bp_person)

####################################
# Using flask-restful
######################################

class PersonResource(Resource):

    person = Person()

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('filter', location="args")
        data = parser.parse_args()

        return data, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('age', location='json', type=int, required=True)
        parser.add_argument('sex', location='json')
        data = parser.parse_args()

        self.person.name = data['name']
        self.person.age = data['age']
        self.person.sex = data['sex']
        return self.person.__dict__, 200, {'Content-Type': 'application/json'}

    def put(self):
        return "This is PUT", 200

    def delete(self):
        return "Deleted", 200

    def patch(self):
        return "Not yet implement", 501

api.add_resource(PersonResource, '')
