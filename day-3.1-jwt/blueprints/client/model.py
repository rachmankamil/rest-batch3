from blueprints import db
from flask_restful import fields


class Clients(db.Model):
	__tablename__ = "client"
	client_key = db.Column(db.String(30), primary_key=True)
	client_name = db.Column(db.String(30), nullable=False)
	client_secret = db.Column(db.String(30), nullable=True)
	status = db.Column(db.Boolean, nullable=False)

	response_fields = {
		'client_key': fields.String,
		'client_name': fields.String,
		'client_secret': fields.String,
		'status': fields.Boolean
	}

	jwt_claims_fields = {
		'client_key': fields.String,
		'status': fields.Boolean
	}

	def __init__(self, id, name, secret, status):
		self.client_key = id
		self.client_name = name
		self.client_secret = secret
		self.status = status

	def __repr__(self):
		return '<Client %r>' % self.client_key
