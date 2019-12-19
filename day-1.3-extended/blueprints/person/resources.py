import json
from flask import Blueprint
from flask_restful import Api, reqparse, Resource

from . import *

bp_person = Blueprint('person', __name__)
api = Api(bp_person)

####################################
# Using flask-restful
######################################

class PersonResource(Resource):

	persons = Persons()

	def __init__(self):
		pass

	def get(self, id=None):
		if id is None:
			return self.persons.get_list(), 200, {'Content-Type': 'application/json'}
		else:
			result = self.persons.get_one(id)
			if result is not None:
				return result, 200, {'Content-Type': 'application/json'}
			else:
				return {'status': 'NOT_FOUND', 'message': 'Person not found'}, 404, {'Content-Type': 'application/json'}

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('name', location='json', required=True)
		parser.add_argument('age', location='json', type=int, required=True)
		parser.add_argument('sex', location='json')
		data = parser.parse_args()

		person = Person()
		person.id = self.persons.persons[-1]['id'] + 1
		person.name = data['name']
		person.age = data['age']
		person.sex = data['sex']

		self.persons.add(person)
		return person.__dict__, 200, {'Content-Type': 'application/json'}

	def put(self, id):
		parser = reqparse.RequestParser()
		parser.add_argument('name', location='json')
		parser.add_argument('age', location='json', type=int)
		parser.add_argument('sex', location='json')
		args = parser.parse_args()

		# person = Person()

		name = args['name']
		age = args['age']
		sex = args['sex']

		result = self.persons.edit_one(id, name, age, sex)
		if result is not None:
			return result.__dict__, 200, {'Content-Type': 'application/json'}
		else:
			return {'status': 'NOT_FOUND', 'message': 'Person not found'}, 404, { 'Content-Type': 'application/json' }

	def delete(self, id):
		result = self.persons.delete_one(id)
		if result is not None:
			return 'deleted', 200, {'Content-Type': 'application/json'}
		else:
			return {'status': 'NOT_FOUND', 'message': 'Person not found'}, 404, { 'Content-Type': 'application/json' }

	def patch(self):
		return "Not yet implement", 501

api.add_resource(PersonResource, '', '/<id>')
