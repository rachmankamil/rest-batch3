from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import  Persons

import hashlib, uuid

from blueprints import db, app

bp_person = Blueprint('person', __name__)
api = Api(bp_person)


####################################
# Using flask-restful
######################################

class PersonResource(Resource):

    def __init__(self):
        pass

    def get(self, id):
        qry = Persons.query.get(id)
        if qry is not None:
            return marshal(qry, Persons.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_name', location='json', required=True)
        parser.add_argument('age', location='json', type=int, required=True)
        parser.add_argument('sex', location='json')
        parser.add_argument('password', location='json')
        args = parser.parse_args()

        salt = uuid.uuid4().hex
        encoded = ('%s%s' % (args['password'], salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encoded).hexdigest()

        person = Persons(args['client_name'], args['age'], args['sex'], salt, hash_pass)
        db.session.add(person)
        db.session.commit()

        app.logger.debug('DEBUG : %s', person)

        return marshal(person, Persons.response_fields), 200, {'Content-Type': 'application/json'}

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('age', location='json', type=int, required=True)
        parser.add_argument('sex', location='json')
        args = parser.parse_args()

        qry = Persons.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        qry.name = args['name']
        qry.age = args['age']
        qry.sex = args['sex']
        db.session.commit()

        return marshal(qry, Persons.response_fields), 200

    def delete(self, id):
        qry = Persons.query.get(id)
        if qry is None:
            return {'status': 'NOT_FOUND'}, 404

        db.session.delete(qry)
        db.session.commit()

        return {'status': 'DELETED'}, 200

class PersonList(Resource):

    def __init__(self):
        pass

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('sex', location='args', help='invalid status', choices=('male', 'female'))
        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=('age', 'sex'))
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'))
        parser.add_argument('status', location='args', choices=('true', 'false', 'True', 'False'))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Persons.query

        if args['sex'] is not None:
            qry = qry.filter_by(sex=args['sex'])

        if args['status'] is not None:
            qry = qry.filter_by(status=True if args['status'].lower()=="true" else False)

        if args['orderby'] is not None:
            if args['orderby'] == 'age':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Persons.age))
                else:
                    qry = qry.order_by(Persons.age)
            elif args['orderby'] == 'sex':
                if args['sort'] == 'desc':
                    qry = qry.order_by(desc(Persons.sex))
                else:
                    qry = qry.order_by(Persons.sex)

        rows = []
        for row in qry.limit(args['rp']).offset(offset).all():
            rows.append(marshal(row, Persons.response_fields))

        return rows, 200
### Routes

api.add_resource(PersonList, '', '/list')
api.add_resource(PersonResource, '', '/<id>')
