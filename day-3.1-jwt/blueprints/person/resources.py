import json
from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal
from flask_jwt_extended import jwt_required
from sqlalchemy import desc

from .model import  Persons
from blueprints import db, app, internal_required

bp_person = Blueprint('person', __name__)
api = Api(bp_person)


####################################
# Using flask-restful
######################################

class PersonResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, id):
        qry = Persons.query.get(id)
        if qry is not None:
            return marshal(qry, Persons.response_fields), 200
        return {'status': 'NOT_FOUND'}, 404

    @jwt_required
    @internal_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', location='json', required=True)
        parser.add_argument('age', location='json', type=int, required=True)
        parser.add_argument('sex', location='json')
        args = parser.parse_args()

        person = Persons(args['name'], args['age'], args['sex'])
        db.session.add(person)
        db.session.commit()

        app.logger.debug('DEBUG : %s', person)

        return marshal(person, Persons.response_fields), 200, {'Content-Type': 'application/json'}

    @jwt_required
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

    @jwt_required
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

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        parser.add_argument('sex', location='args', help='invalid status', choices=('male', 'female'))
        parser.add_argument('orderby', location='args', help='invalid orderby value', choices=('age', 'sex'))
        parser.add_argument('sort', location='args', help='invalid sort value', choices=('desc', 'asc'))
        args = parser.parse_args()

        offset = (args['p'] * args['rp']) - args['rp']

        qry = Persons.query

        if args['sex'] is not None:
            qry = qry.filter_by(sex=args['sex'])

        claims = jwt_get_claims()
        qry = qry.filter_by(client_id=claims['client_id'])

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
