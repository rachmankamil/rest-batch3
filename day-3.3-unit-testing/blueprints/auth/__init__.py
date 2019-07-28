from flask import Blueprint
from flask_restful import Api, Resource, reqparse

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

### Resources
class CreateTokenResource(Resource):

    def post(self):
        ## Create token
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='json', required=True)
        parser.add_argument('client_secret', location='json', required=True)
        args = parser.parse_args()

        if args['client_key'] == 'altarest' and args['client_secret'] == '1OopwAPk3Q2D':
            token = create_access_token(identity=args['client_key'])
        else:
            return {'status': 'UNAUTHORIZED', 'message': 'invalid key or secret'}, 401

        return {'token': token}, 200

    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        return {'claims': claims}, 200

class RefreshTokenResource(Resource):

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        token = create_access_token(identity=current_user)
        return {'token': token}, 200

### Routes
api.add_resource(CreateTokenResource, '')
api.add_resource(RefreshTokenResource, '/refresh')
