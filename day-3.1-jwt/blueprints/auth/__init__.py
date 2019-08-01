from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

from ..client.model import Clients

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

### Resources
class CreateTokenResource(Resource):

    def get(self):
        ## Create token
        parser = reqparse.RequestParser()
        parser.add_argument('client_key', location='args', required=True)
        parser.add_argument('client_secret', location='args', required=True)
        args = parser.parse_args()

        qry = Clients.query.filter_by(client_id=args['client_key']).filter_by(client_secret=args['client_secret'])

        clientData = qry.first()
        if clientData is not None :
            clientData = marshal(clientData, Clients.jwt_claims_fields)
            # clientData.pop("client_secret")
            token = create_access_token(identity=args['client_key'], user_claims=clientData)
            return {'token': token}, 200
        else:
            return {'status': 'UNAUTHORIZED', 'message': 'invalid key or secret'}, 401

        # if args['client_key'] == 'altarest' and args['client_secret'] == '1OopwAPk3Q2D':
        #     token = create_access_token(identity=args['client_key'])
        # else:
        #     return {'status': 'UNAUTHORIZED', 'message': 'invalid key or secret'}, 401

    @jwt_required
    def post(self):
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
