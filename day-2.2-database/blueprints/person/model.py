from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime

class Persons(db.Model):
	__tablename__ = "person"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(30), unique=True, nullable=False)
	age = db.Column(db.Integer, nullable=True, default=20)
	sex = db.Column(db.String(10), nullable=False)
	password = db.Column(db.String(255))
	salt = db.Column(db.String(255))
	created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
	updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
	deleted_at = db.Column(db.DateTime, server_default=text("0"))

	response_fields = {
		'id': fields.Integer,
		'name': fields.String,
		'age': fields.Integer,
		'sex': fields.String,
		'password': fields.String
	}

	def __init__(self, person_name, age, sex, salt, password):
		self.name = person_name
		self.age = age
		self.sex = sex
		self.salt = salt
		self.password = password

	def __repr__(self):
		return '<Person %r>' % self.id
