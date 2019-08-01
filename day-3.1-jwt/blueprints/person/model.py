from blueprints import db
from flask_restful import fields

class Persons(db.Model):
	__tablename__ = "person"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(30), unique=True, nullable=False)
	age = db.Column(db.Integer, nullable=True, default=20)
	sex = db.Column(db.String(10), nullable=False)

	response_fields = {
		'id': fields.Integer,
		'name': fields.String,
		'age': fields.Integer,
		'sex': fields.String
	}

	def __init__(self, person_name, age, sex):
		self.name = person_name
		self.age = age
		self.sex = sex

	def __repr__(self):
		return '<Person %r>' % self.id
